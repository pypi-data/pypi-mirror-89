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
import audioop
from time import sleep, time as get_time

from collections import deque
import os
from os.path import isdir, join
import pyaudio
import speech_recognition
from hashlib import md5
from speech_recognition import (
    Microphone,
    AudioSource,
    AudioData
)
import json
from threading import Lock

from mycroft_voice_satellite.configuration import CONFIGURATION
from mycroft_voice_satellite.speech.signal import check_for_signal
from mycroft_voice_satellite.playback import play_audio, play_mp3, play_ogg, \
    play_wav, resolve_resource_file
from ovos_utils.log import LOG
from ovos_utils.lang.phonemes import get_phonemes


class MutableStream:
    def __init__(self, wrapped_stream, format, muted=False):
        assert wrapped_stream is not None
        self.wrapped_stream = wrapped_stream

        self.muted = muted
        if muted:
            self.mute()

        self.SAMPLE_WIDTH = pyaudio.get_sample_size(format)
        self.muted_buffer = b''.join([b'\x00' * self.SAMPLE_WIDTH])
        self.read_lock = Lock()

    def mute(self):
        """Stop the stream and set the muted flag."""
        with self.read_lock:
            self.muted = True
            self.wrapped_stream.stop_stream()

    def unmute(self):
        """Start the stream and clear the muted flag."""
        with self.read_lock:
            self.muted = False
            self.wrapped_stream.start_stream()

    def read(self, size, of_exc=False):
        """Read data from stream.

        Arguments:
            size (int): Number of bytes to read
            of_exc (bool): flag determining if the audio producer thread
                           should throw IOError at overflows.

        Returns:
            (bytes) Data read from device
        """
        frames = deque()
        remaining = size
        with self.read_lock:
            while remaining > 0:
                # If muted during read return empty buffer. This ensures no
                # reads occur while the stream is stopped
                if self.muted:
                    return self.muted_buffer

                to_read = min(self.wrapped_stream.get_read_available(),
                              remaining)
                if to_read <= 0:
                    sleep(.01)
                    continue
                result = self.wrapped_stream.read(to_read,
                                                  exception_on_overflow=of_exc)
                frames.append(result)
                remaining -= to_read

        input_latency = self.wrapped_stream.get_input_latency()
        if input_latency > 0.2:
            LOG.warning("High input latency: %f" % input_latency)
        audio = b"".join(list(frames))
        return audio

    def close(self):
        self.wrapped_stream.close()
        self.wrapped_stream = None

    def is_stopped(self):
        try:
            return self.wrapped_stream.is_stopped()
        except Exception as e:
            LOG.error(repr(e))
            return True  # Assume the stream has been closed and thusly stopped

    def stop_stream(self):
        return self.wrapped_stream.stop_stream()


class MutableMicrophone(Microphone):
    def __init__(self, device_index=None, sample_rate=16000, chunk_size=1024,
                 mute=False):
        Microphone.__init__(self, device_index=device_index,
                            sample_rate=sample_rate, chunk_size=chunk_size)
        self.muted = False
        if mute:
            self.mute()

    def __enter__(self):
        return self._start()

    def _start(self):
        """Open the selected device and setup the stream."""
        assert self.stream is None, \
            "This audio source is already inside a context manager"
        self.audio = pyaudio.PyAudio()
        self.stream = MutableStream(self.audio.open(
            input_device_index=self.device_index, channels=1,
            format=self.format, rate=self.SAMPLE_RATE,
            frames_per_buffer=self.CHUNK,
            input=True,  # stream is an input stream
        ), self.format, self.muted)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._stop()

    def _stop(self):
        """Stop and close an open stream."""
        try:
            if not self.stream.is_stopped():
                self.stream.stop_stream()
            self.stream.close()
        except Exception:
            LOG.exception('Failed to stop mic input stream')
            # Let's pretend nothing is wrong...

        self.stream = None
        self.audio.terminate()

    def restart(self):
        """Shutdown input device and restart."""
        self._stop()
        self._start()

    def mute(self):
        self.muted = True
        if self.stream:
            self.stream.mute()

    def unmute(self):
        self.muted = False
        if self.stream:
            self.stream.unmute()

    def is_muted(self):
        return self.muted


def get_silence(num_bytes):
    return b'\0' * num_bytes


class ResponsiveRecognizer(speech_recognition.Recognizer):
    # Padding of silence when feeding to pocketsphinx
    SILENCE_SEC = 0.01

    def __init__(self, hot_word_engines):

        self.config = CONFIGURATION
        listener_config = self.config.get('listener')

        self.overflow_exc = listener_config.get('overflow_exception', False)

        speech_recognition.Recognizer.__init__(self)
        self.audio = pyaudio.PyAudio()
        self.multiplier = listener_config.get('multiplier')
        self.energy_ratio = listener_config.get('energy_ratio')
        self.sec_between_ww_checks = \
            listener_config.get("sec_between_ww_checks", 0.2)
        self.recording_timeout_with_silence = \
            listener_config.get("recording_timeout_with_silence", 3.0)
        self.recording_timeout = listener_config.get("recording_timeout", 10.0)
        self.min_loud_sec = listener_config.get("min_loud_sec", 0.5)
        self.min_silence_at_end = \
            listener_config.get("min_silence_at_end", 0.25)
        self.ambient_noise_adjustment_time = listener_config.get(
            "ambient_noise_adjustment_time", 0.5)
        self.auto_ambient_noise_adjustment = listener_config.get(
            "auto_ambient_noise_adjustment", False)

        # check the config for the flag to save wake words.
        data_path = os.path.expanduser(self.config["data_dir"])
        self.save_wake_words = listener_config.get('record_wake_words', False)
        self.saved_wake_words_dir = join(data_path, 'hotwords')
        if not os.path.isdir(data_path):
            os.makedirs(data_path)
        if not os.path.isdir(self.saved_wake_words_dir):
            os.makedirs(self.saved_wake_words_dir)

        # Signal statuses
        self._stop_signaled = False
        self._listen_triggered = False
        self._should_adjust_noise = False

        self.hotword_engines = hot_word_engines or {}
        # The maximum audio in seconds to keep for transcribing a phrase
        # The wake word must fit in this time
        num_phonemes = 10
        # use number of phonemes from longest hotword
        for w in self.hotword_engines:
            phon = get_phonemes(w).split(" ")
            if len(phon) > num_phonemes:
                num_phonemes = len(phon)

        len_phoneme = listener_config.get('phoneme_duration', 120) / 1000.0
        self.TEST_WW_SEC = num_phonemes * len_phoneme
        self.SAVED_WW_SEC = max(3, self.TEST_WW_SEC)

    def feed_hotwords(self, chunk):
        """ feed sound chunk to hotword engines that perform streaming
        predictions (precise) """
        for hw in self.hotword_engines:
            self.hotword_engines[hw]["engine"].update(chunk)

    def record_sound_chunk(self, source):
        return source.stream.read(source.CHUNK, self.overflow_exc)

    @staticmethod
    def calc_energy(sound_chunk, sample_width):
        return audioop.rms(sound_chunk, sample_width)

    def _record_phrase(
        self,
        source,
        sec_per_buffer,
        stream=None,
        ww_frames=None
    ):
        """Record an entire spoken phrase.

        Essentially, this code waits for a period of silence and then returns
        the audio.  If silence isn't detected, it will terminate and return
        a buffer of RECORDING_TIMEOUT duration.

        Args:
            source (AudioSource):  Source producing the audio chunks
            sec_per_buffer (float):  Fractional number of seconds in each chunk
            stream (AudioStreamHandler): Stream target that will receive chunks
                                         of the utterance audio while it is
                                         being recorded.
            ww_frames (deque):  Frames of audio data from the last part of wake
                                word detection.

        Returns:
            bytearray: complete audio buffer recorded, including any
                       silence at the end of the user's utterance
        """

        num_loud_chunks = 0
        noise = 0

        max_noise = 25
        min_noise = 0

        silence_duration = 0

        def increase_noise(level):
            if level < max_noise:
                return level + 200 * sec_per_buffer
            return level

        def decrease_noise(level):
            if level > min_noise:
                return level - 100 * sec_per_buffer
            return level

        # Smallest number of loud chunks required to return
        min_loud_chunks = int(self.min_loud_sec / sec_per_buffer)

        # Maximum number of chunks to record before timing out
        max_chunks = int(self.recording_timeout / sec_per_buffer)
        num_chunks = 0

        # Will return if exceeded this even if there's not enough loud chunks
        max_chunks_of_silence = int(self.recording_timeout_with_silence /
                                    sec_per_buffer)

        # bytearray to store audio in
        byte_data = get_silence(source.SAMPLE_WIDTH)

        if stream:
            stream.stream_start()

        phrase_complete = False
        while num_chunks < max_chunks and not phrase_complete:
            if ww_frames:
                chunk = ww_frames.popleft()
            else:
                chunk = self.record_sound_chunk(source)
            byte_data += chunk
            num_chunks += 1

            if stream:
                stream.stream_chunk(chunk)

            energy = self.calc_energy(chunk, source.SAMPLE_WIDTH)
            test_threshold = self.energy_threshold * self.multiplier
            is_loud = energy > test_threshold
            if is_loud:
                noise = increase_noise(noise)
                num_loud_chunks += 1
            else:
                noise = decrease_noise(noise)
                self._adjust_threshold(energy, sec_per_buffer)

            was_loud_enough = num_loud_chunks > min_loud_chunks

            quiet_enough = noise <= min_noise
            if quiet_enough:
                silence_duration += sec_per_buffer
                if silence_duration < self.min_silence_at_end:
                    quiet_enough = False  # gotta be silent for min of 1/4 sec
            else:
                silence_duration = 0
            recorded_too_much_silence = num_chunks > max_chunks_of_silence
            if quiet_enough and (was_loud_enough or recorded_too_much_silence):
                phrase_complete = True

            # Pressing top-button will end recording immediately
            if check_for_signal('buttonPress'):
                phrase_complete = True

        return byte_data

    @staticmethod
    def sec_to_bytes(sec, source):
        return int(sec * source.SAMPLE_RATE) * source.SAMPLE_WIDTH

    def _skip_wake_word(self, source):
        """Check if told programatically to skip the wake word

        For example when we are in a dialog with the user.
        """

        signaled = False
        if check_for_signal('startListening') or self._listen_triggered:
            signaled = True

        # Pressing the Mark 1 button can start recording (unless
        # it is being used to mean 'stop' instead)
        elif check_for_signal('buttonPress', 1):
            # give other processes time to consume this signal if
            # it was meant to be a 'stop'
            sleep(0.25)
            if check_for_signal('buttonPress'):
                # Signal is still here, assume it was intended to
                # begin recording
                LOG.debug("Button Pressed, wakeword not needed")
                signaled = True

        if signaled:
            LOG.info("Listen signal detected")
            # If enabled, play a wave file with a short sound to audibly
            # indicate listen signal was detected.
            sound = self.config["listener"].get('listen_sound')
            audio_file = resolve_resource_file(sound)
            if audio_file:
                try:

                    source.mute()
                    if audio_file.endswith(".wav"):
                        play_wav(audio_file).wait()
                    elif audio_file.endswith(".mp3"):
                        play_mp3(audio_file).wait()
                    elif audio_file.endswith(".ogg"):
                        play_ogg(audio_file).wait()
                    else:
                        play_audio(audio_file).wait()
                    source.unmute()
                except Exception as e:
                    LOG.warning(e)

        return signaled

    def stop(self):
        """
            Signal stop and exit waiting state.
        """
        self._stop_signaled = True

    def _compile_metadata(self, hw):
        ww_module = self.hotword_engines[hw]["engine"].__class__.__name__
        if ww_module == 'PreciseHotword':
            model_path = self.hotword_engines[hw]["engine"].precise_model
            with open(model_path, 'rb') as f:
                model_hash = md5(f.read()).hexdigest()
        else:
            model_hash = '0'

        return {
            'name': self.hotword_engines[hw]["engine"].key_phrase.replace(' ', '-'),
            'engine': md5(ww_module.encode('utf-8')).hexdigest(),
            'time': str(int(1000 * get_time())),
            'model': str(model_hash)
        }

    def trigger_listen(self):
        """Externally trigger listening."""
        LOG.debug('Listen triggered from external source.')
        self._listen_triggered = True

    def trigger_ambient_noise_adjustment(self):
        LOG.debug("Ambient noise adjustment requested from external source")
        self._should_adjust_noise = True

    def _adjust_ambient_noise(self, source, time=None):
        time = time or self.ambient_noise_adjustment_time
        LOG.info("Adjusting for ambient noise, be silent!!!")
        self.adjust_for_ambient_noise(source, time)
        LOG.info("Ambient noise profile has been created")
        self._should_adjust_noise = False

    def _wait_until_wake_word(self, source, sec_per_buffer, bus):
        """Listen continuously on source until a wake word is spoken

        Args:
            source (AudioSource):  Source producing the audio chunks
            sec_per_buffer (float):  Fractional number of seconds in each chunk
        """
        num_silent_bytes = int(self.SILENCE_SEC * source.SAMPLE_RATE *
                               source.SAMPLE_WIDTH)

        silence = get_silence(num_silent_bytes)

        # bytearray to store audio in
        byte_data = silence

        buffers_per_check = self.sec_between_ww_checks / sec_per_buffer
        buffers_since_check = 0.0

        # Max bytes for byte_data before audio is removed from the front
        max_size = self.sec_to_bytes(self.SAVED_WW_SEC, source)
        test_size = self.sec_to_bytes(self.TEST_WW_SEC, source)

        said_wake_word = False

        # Rolling buffer to track the audio energy (loudness) heard on
        # the source recently.  An average audio energy is maintained
        # based on these levels.
        energies = []
        idx_energy = 0
        avg_energy = 0.0
        energy_avg_samples = int(5 / sec_per_buffer)  # avg over last 5 secs
        counter = 0

        # These are frames immediately after wake word is detected
        # that we want to keep to send to STT
        ww_frames = deque(maxlen=7)

        while not said_wake_word and not self._stop_signaled:
            if self._skip_wake_word(source):
                break
            chunk = self.record_sound_chunk(source)
            ww_frames.append(chunk)

            energy = self.calc_energy(chunk, source.SAMPLE_WIDTH)
            if energy < self.energy_threshold * self.multiplier:
                self._adjust_threshold(energy, sec_per_buffer)

            if len(energies) < energy_avg_samples:
                # build the average
                energies.append(energy)
                avg_energy += float(energy) / energy_avg_samples
            else:
                # maintain the running average and rolling buffer
                avg_energy -= float(energies[idx_energy]) / energy_avg_samples
                avg_energy += float(energy) / energy_avg_samples
                energies[idx_energy] = energy
                idx_energy = (idx_energy + 1) % energy_avg_samples

                # maintain the threshold using average
                if energy < avg_energy * 1.5:
                    if energy > self.energy_threshold:
                        # bump the threshold to just above this value
                        self.energy_threshold = energy * 1.2

            counter += 1

            # At first, the buffer is empty and must fill up.  After that
            # just drop the first chunk bytes to keep it the same size.
            needs_to_grow = len(byte_data) < max_size
            if needs_to_grow:
                byte_data += chunk
            else:  # Remove beginning of audio and add new chunk to end
                byte_data = byte_data[len(chunk):] + chunk

            buffers_since_check += 1.0
            self.feed_hotwords(chunk)
            if buffers_since_check > buffers_per_check:
                buffers_since_check -= buffers_per_check
                chopped = byte_data[-test_size:] \
                    if test_size < len(byte_data) else byte_data
                audio_data = chopped + silence
                said_hot_word = False
                for hotword in self.check_for_hotwords(audio_data, bus):
                    said_hot_word = True
                    engine = self.hotword_engines[hotword]["engine"]
                    sound = self.hotword_engines[hotword]["sound"]
                    utterance = self.hotword_engines[hotword]["utterance"]
                    listen = self.hotword_engines[hotword]["listen"]

                    LOG.debug("Hot Word: " + hotword)
                    # If enabled, play a wave file with a short sound to audibly
                    # indicate hotword was detected.
                    if sound:
                        try:
                            audio_file = resolve_resource_file(sound)
                            source.mute()
                            if audio_file.endswith(".wav"):
                                play_wav(audio_file).wait()
                            elif audio_file.endswith(".mp3"):
                                play_mp3(audio_file).wait()
                            elif audio_file.endswith(".ogg"):
                                play_ogg(audio_file).wait()
                            else:
                                play_audio(audio_file).wait()
                            source.unmute()
                        except Exception as e:
                            LOG.warning(e)

                    # Hot Word succeeded
                    payload = {
                        'hotword': hotword,
                        'start_listening': listen,
                        'sound': sound,
                        "engine": engine.__class__.__name__
                    }
                    bus.emit("recognizer_loop:hotword", payload)

                    if utterance:
                        # send the transcribed word on for processing
                        payload = {
                            'utterances': [utterance]
                        }
                        bus.emit("recognizer_loop:utterance", payload)

                    audio = None
                    mtd = self._compile_metadata(hotword)
                    if self.save_wake_words:
                        # Save wake word locally
                        audio = self._create_audio_data(byte_data, source)

                        if not isdir(self.saved_wake_words_dir):
                            os.mkdir(self.saved_wake_words_dir)

                        fn = join(
                            self.saved_wake_words_dir,
                            '_'.join(str(mtd[k]) for k in sorted(mtd)) + '.wav'
                        )
                        with open(fn, 'wb') as f:
                            f.write(audio.get_wav_data())

                        fn = join(
                            self.saved_wake_words_dir,
                            '_'.join(str(mtd[k]) for k in sorted(mtd)) +
                            '.json'
                        )
                        with open(fn, 'w') as f:
                            json.dump(mtd, f, indent=4)

                    if listen:
                        said_wake_word = True

                if said_hot_word:
                    # reset bytearray to store wake word audio in, else many
                    # serial detections
                    byte_data = silence

    def check_for_hotwords(self, audio_data, bus):
        # check hot word
        for hotword in self.hotword_engines:
            engine = self.hotword_engines[hotword]["engine"]
            if engine.found_wake_word(audio_data):
                yield hotword

    @staticmethod
    def _create_audio_data(raw_data, source):
        """
        Constructs an AudioData instance with the same parameters
        as the source and the specified frame_data
        """
        return AudioData(raw_data, source.SAMPLE_RATE, source.SAMPLE_WIDTH)

    def listen(self, source, bus, stream=None):
        """Listens for chunks of audio that Mycroft should perform STT on.

        This will listen continuously for a wake-up-word, then return the
        audio chunk containing the spoken phrase that comes immediately
        afterwards.

        Args:
            source (AudioSource):  Source producing the audio chunks
            bus (EventEmitter): Emitter for notifications of when recording
                                    begins and ends.
            stream (AudioStreamHandler): Stream target that will receive chunks
                                         of the utterance audio while it is
                                         being recorded

        Returns:
            AudioData: audio with the user's utterance, minus the wake-up-word
        """
        assert isinstance(source, AudioSource), "Source must be an AudioSource"

        #        bytes_per_sec = source.SAMPLE_RATE * source.SAMPLE_WIDTH
        sec_per_buffer = float(source.CHUNK) / source.SAMPLE_RATE

        LOG.debug("Waiting for wake word...")
        self._wait_until_wake_word(source, sec_per_buffer, bus)
        self._listen_triggered = False
        if self._stop_signaled:
            return

        LOG.debug("Recording...")
        bus.emit("recognizer_loop:record_begin")

        frame_data = self._record_phrase(source, sec_per_buffer, stream)
        audio_data = self._create_audio_data(frame_data, source)
        bus.emit("recognizer_loop:record_end")
        if self.auto_ambient_noise_adjustment:
            self._adjust_ambient_noise(source)
        LOG.debug("Thinking...")
        return audio_data

    def _adjust_threshold(self, energy, seconds_per_buffer):
        if self.dynamic_energy_threshold and energy > 0:
            # account for different chunk sizes and rates
            damping = (
                    self.dynamic_energy_adjustment_damping ** seconds_per_buffer)
            target_energy = energy * self.energy_ratio
            self.energy_threshold = (
                    self.energy_threshold * damping +
                    target_energy * (1 - damping))
