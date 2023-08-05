# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import re
import os
import time
from time import sleep, time as get_time
import json
from threading import Thread
import speech_recognition as sr
import pyaudio
from pyee import EventEmitter
from requests import RequestException
from requests.exceptions import ConnectionError
from mycroft_voice_satellite.configuration import CONFIGURATION
from mycroft_voice_satellite.speech.hotword_factory import HotWordFactory
from mycroft_voice_satellite.speech.mic import MutableMicrophone, \
    ResponsiveRecognizer
from speech2text import STTFactory
from queue import Queue, Empty
from ovos_utils.log import LOG
from mycroft_voice_satellite.playback import play_audio, play_mp3, play_ogg, \
    play_wav, resolve_resource_file

MAX_MIC_RESTARTS = 20


AUDIO_DATA = 0
STREAM_START = 1
STREAM_DATA = 2
STREAM_STOP = 3


def find_input_device(device_name):
    """ Find audio input device by name.

        Arguments:
            device_name: device name or regex pattern to match

        Returns: device_index (int) or None if device wasn't found
    """
    LOG.info('Searching for input device: {}'.format(device_name))
    LOG.debug('Devices: ')
    pa = pyaudio.PyAudio()
    pattern = re.compile(device_name)
    for device_index in range(pa.get_device_count()):
        dev = pa.get_device_info_by_index(device_index)
        LOG.debug('   {}'.format(dev['name']))
        if dev['maxInputChannels'] > 0 and pattern.match(dev['name']):
            LOG.debug('    ^-- matched')
            return device_index
    return None


class AudioStreamHandler:
    def __init__(self, queue):
        self.queue = queue

    def stream_start(self):
        self.queue.put((STREAM_START, None, None))

    def stream_chunk(self, chunk, source=None):
        self.queue.put((STREAM_DATA, chunk, source))

    def stream_stop(self):
        self.queue.put((STREAM_STOP, None, None))


class AudioProducer(Thread):
    """AudioProducer
    Given a mic and a recognizer implementation, continuously listens to the
    mic for potential speech chunks and pushes them onto the queue.
    """

    def __init__(self, state, queue, mic, recognizer, emitter, stream_handler):
        super(AudioProducer, self).__init__()
        self.daemon = True
        self.state = state
        self.queue = queue
        self.mic = mic
        self.recognizer = recognizer
        self.emitter = emitter
        self.stream_handler = stream_handler

    def run(self):
        restart_attempts = 0
        with self.mic as source:
            LOG.info("Adjusting for ambient noise, be silent!!!")
            self.recognizer.adjust_for_ambient_noise(source)
            LOG.info("Ambient noise profile has been created")
            while self.state.running:
                try:
                    audio = self.recognizer.listen(source, self.emitter,
                                                   self.stream_handler)
                    if audio is not None:
                        self.queue.put((AUDIO_DATA, audio, source))
                    else:
                        LOG.warning("Audio contains no data.")
                except IOError as e:
                    # IOError will be thrown if the read is unsuccessful.
                    # If self.recognizer.overflow_exc is False (default)
                    # input buffer overflow IOErrors due to not consuming the
                    # buffers quickly enough will be silently ignored.
                    LOG.exception('IOError Exception in AudioProducer')
                    if e.errno == pyaudio.paInputOverflowed:
                        pass  # Ignore overflow errors
                    elif restart_attempts < MAX_MIC_RESTARTS:
                        # restart the mic
                        restart_attempts += 1
                        LOG.info('Restarting the microphone...')
                        source.restart()
                        LOG.info('Restarted...')
                    else:
                        LOG.error('Restarting mic doesn\'t seem to work. '
                                  'Stopping...')
                        raise
                except Exception:
                    LOG.exception('Exception in AudioProducer')
                    raise
                else:
                    # Reset restart attempt counter on sucessful audio read
                    restart_attempts = 0
                finally:
                    if self.stream_handler is not None:
                        self.stream_handler.stream_stop()

    def stop(self):
        """Stop producer thread."""
        self.state.running = False
        self.recognizer.stop()


class AudioConsumer(Thread):
    """AudioConsumer
    Consumes AudioData chunks off the queue
    """

    # In seconds, the minimum audio size to be sent to remote STT
    MIN_AUDIO_SIZE = 0.5

    def __init__(self, state, queue, emitter, stt, wakeup_recognizer):
        super(AudioConsumer, self).__init__()
        self.daemon = True
        self.queue = queue
        self.state = state
        self.emitter = emitter
        self.stt = stt
        self.wakeup_recognizer = wakeup_recognizer
        data_path = os.path.expanduser(CONFIGURATION["data_dir"])
        listener_config = CONFIGURATION["listener"]
        self.save_utterances = listener_config.get('record_utterances', False)
        self.saved_utterances_dir = os.path.join(data_path, 'utterances')
        if not os.path.isdir(data_path):
            os.makedirs(data_path)
        if not os.path.isdir(self.saved_utterances_dir):
            os.makedirs(self.saved_utterances_dir)

    def run(self):
        while self.state.running:
            self.read()

    def read(self):
        try:
            audio = self.queue.get(timeout=0.5)
        except Empty:
            return

        if audio is None:
            return

        tag, data, source = audio

        if tag == AUDIO_DATA:
            if data is not None:
                if self.state.sleeping:
                    self.wake_up(data)
                else:
                    self.process(data, source)
        elif tag == STREAM_START:
            self.stt.stream_start()
        elif tag == STREAM_DATA:
            self.stt.stream_data(data)
        elif tag == STREAM_STOP:
            self.stt.stream_stop()
        else:
            LOG.error("Unknown audio queue type %r" % audio)

    def wake_up(self, audio):
        if self.wakeup_recognizer.found_wake_word(audio.frame_data):
            self.state.sleeping = False
            self.emitter.emit('recognizer_loop:awoken')

    @staticmethod
    def _audio_length(audio):
        return float(len(audio.frame_data)) / (
                audio.sample_rate * audio.sample_width)

    # TODO: Localization
    def process(self, audio, source=None):
        if source:
            LOG.debug("Muting microphone during STT")
            source.mute()
        if self._audio_length(audio) < self.MIN_AUDIO_SIZE:
            LOG.warning("Audio too short to be processed")
        else:
            transcription = self.transcribe(audio)
            if transcription:
                # STT succeeded, send the transcribed speech on for processing
                payload = {
                    'utterances': [transcription],
                    'lang': self.stt.lang
                }
                self.emitter.emit("recognizer_loop:utterance", payload)
        if source:
            LOG.debug("Unmuting microphone")
            source.unmute()

    def _compile_metadata(self, utterance):
        timestamp = str(int(1000 * get_time()))
        if utterance:
            name = utterance.replace(" ", "_").lower() + "_" + timestamp + ".wav"
        else:
            name = "UNK_" + timestamp + ".wav"
        return {
            'name': name,
            'transcript': utterance,
            'engine': self.stt.__class__.__name__,
            'time': timestamp
        }

    @staticmethod
    def play_error():
        # If enabled, play a wave file with a short sound to audibly
        # indicate speech recognition failed
        sound = CONFIGURATION["listener"].get('error_sound')
        audio_file = resolve_resource_file(sound)
        if audio_file:
            try:
                if audio_file.endswith(".wav"):
                    play_wav(audio_file).wait()
                elif audio_file.endswith(".mp3"):
                    play_mp3(audio_file).wait()
                elif audio_file.endswith(".ogg"):
                    play_ogg(audio_file).wait()
                else:
                    play_audio(audio_file).wait()
            except Exception as e:
                LOG.warning(e)

    def save_utt(self, text, audio):
        if self.save_utterances:
            LOG.debug("saving utterance")
            mtd = self._compile_metadata(text)

            filename = os.path.join(self.saved_utterances_dir, mtd["name"])
            with open(filename, 'wb') as f:
                f.write(audio.get_wav_data())

            filename = os.path.join(self.saved_utterances_dir,
                                    mtd["name"].replace(".wav", ".json"))
            with open(filename, 'w') as f:
                json.dump(mtd, f, indent=4)

    def transcribe(self, audio):
        def send_unknown_intent():
            """ Send message that nothing was transcribed. """
            self.emitter.emit('recognizer_loop:speech.recognition.unknown')

        try:
            # Invoke the STT engine on the audio clip
            text = self.stt.execute(audio)
            if text is not None:
                text = text.lower().strip()
                LOG.debug("STT: " + text)
            else:
                send_unknown_intent()
                LOG.info('no words were transcribed')
            self.save_utt(text, audio)
            return text
        except sr.RequestError as e:
            LOG.error("Could not request Speech Recognition {0}".format(e))
        except ConnectionError as e:
            LOG.error("Connection Error: {0}".format(e))
            self.emitter.emit("recognizer_loop:no_internet")
        except RequestException as e:
            LOG.error(e.__class__.__name__ + ': ' + str(e))
        except sr.UnknownValueError:
            LOG.error("Speech Recognition could not understand audio")
        except Exception as e:
            send_unknown_intent()
            LOG.exception(e)
            LOG.error("Speech Recognition Error")
        self.play_error()
        self.save_utt("", audio)
        return None


class RecognizerLoopState:
    def __init__(self):
        self.running = False
        self.sleeping = False


class RecognizerLoop(EventEmitter):
    """ EventEmitter loop running speech recognition.

    Local wake word recognizer and remote general speech recognition.
    """

    def __init__(self, config=None):
        super(RecognizerLoop, self).__init__()
        self.mute_calls = 0
        self.config = config or CONFIGURATION
        self._load_config(config)

    def _load_config(self, config=None):
        """Load configuration parameters from configuration."""
        config = config or self.config
        self.config_core = config
        self.lang = config.get('lang')
        self.config = config.get('listener')
        rate = self.config.get('sample_rate')

        device_index = self.config.get('device_index')
        device_name = self.config.get('device_name')
        if not device_index and device_name:
            device_index = find_input_device(device_name)

        LOG.debug('Using microphone (None = default): ' + str(device_index))

        self.microphone = MutableMicrophone(device_index, rate,
                                            mute=self.mute_calls > 0)

        # TODO - localization
        self.wakeup_recognizer = self.create_wakeup_recognizer()
        self.hotword_engines = {}
        self.create_hotword_engines()
        self.responsive_recognizer = ResponsiveRecognizer(self.hotword_engines)
        self.state = RecognizerLoopState()

    def create_hotword_engines(self):
        LOG.info("creating hotword engines")
        hot_words = self.config_core.get("hotwords", {})
        for word in hot_words:
            data = hot_words[word]
            if word == self.wakeup_recognizer.key_phrase \
                    or not data.get("active", True):
                continue
            sound = data.get("sound")
            utterance = data.get("utterance")
            listen = data.get("listen", False)
            engine = HotWordFactory.create_hotword(word, lang=self.lang)

            self.hotword_engines[word] = {"engine": engine,
                                          "sound": sound,
                                          "utterance": utterance,
                                          "listen": listen}

    def create_wakeup_recognizer(self):
        LOG.info("creating stand up word engine")
        word = self.config.get("stand_up_word", "wake up")
        return HotWordFactory.create_hotword(word, lang=self.lang, loop=self)

    def start_async(self):
        """Start consumer and producer threads."""
        self.state.running = True
        stt = STTFactory.create(self.config_core["stt"])
        queue = Queue()
        stream_handler = None
        if stt.can_stream:
            stream_handler = AudioStreamHandler(queue)
        LOG.debug("Using STT engine: " + stt.__class__.__name__)
        self.producer = AudioProducer(self.state, queue, self.microphone,
                                      self.responsive_recognizer, self,
                                      stream_handler)
        self.producer.start()
        self.consumer = AudioConsumer(self.state, queue, self,
                                      stt, self.wakeup_recognizer)
        self.consumer.start()

    def stop(self):
        self.state.running = False
        self.producer.stop()
        # wait for threads to shutdown
        self.producer.join()
        self.consumer.join()

    def mute(self):
        """Mute microphone and increase number of requests to mute."""
        self.mute_calls += 1
        if self.microphone:
            self.microphone.mute()

    def unmute(self):
        """Unmute mic if as many unmute calls as mute calls have been received.
        """
        if self.mute_calls > 0:
            self.mute_calls -= 1

        if self.mute_calls <= 0 and self.microphone:
            self.microphone.unmute()
            self.mute_calls = 0

    def force_unmute(self):
        """Completely unmute mic regardless of the number of calls to mute."""
        self.mute_calls = 0
        self.unmute()

    def is_muted(self):
        if self.microphone:
            return self.microphone.is_muted()
        else:
            return True  # consider 'no mic' muted

    def sleep(self):
        self.state.sleeping = True

    def awaken(self):
        self.state.sleeping = False

    def run(self):
        """Start and reload mic and STT handling threads as needed.

        Wait for KeyboardInterrupt and shutdown cleanly.
        """
        try:
            self.start_async()
        except Exception:
            LOG.exception('Starting producer/consumer threads for listener '
                          'failed.')
            return

        # Handle reload of consumer / producer if config changes
        while self.state.running:
            try:
                time.sleep(1)
            except KeyboardInterrupt as e:
                LOG.error(e)
                self.stop()
                raise  # Re-raise KeyboardInterrupt
            except Exception:
                LOG.exception('Exception in RecognizerLoop')
                raise

    def reload(self):
        """Reload configuration and restart consumer and producer."""
        self.stop()
        for hw in self.hotword_engines:
            try:
                self.hotword_engines[hw]["engine"].stop()
            except Exception as e:
                LOG.exception(e)
        # load config
        self._load_config()
        # restart
        self.start_async()
