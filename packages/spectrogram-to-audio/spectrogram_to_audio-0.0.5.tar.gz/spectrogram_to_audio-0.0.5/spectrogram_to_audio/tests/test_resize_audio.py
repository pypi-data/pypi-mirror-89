from unittest import TestCase
import tensorflow as tf
import random

from config.load_config import config
from spectrogram_to_audio.data_preprocessing.dataset import get_dataset, resize_audio


class TestResizeAudio(TestCase):

    def test_resize_audio(self):

        def get_random_audio():
            gen_audio_len = random.randint(1000, 100000)
            return tf.random.uniform(
                [gen_audio_len], minval=-1, maxval=1, dtype=tf.dtypes.float32
            )

        def get_gen_audios():
            audios =[]
            for i in range(10):
                audios.append(
                    get_random_audio()
                )
            return audios

        for audio in get_gen_audios():
            audio_size = config.AUDIO.SAMPLE_RATE * config.AUDIO.AUDIO_TIME_SEC
            assert(resize_audio(audio).shape == (audio_size))