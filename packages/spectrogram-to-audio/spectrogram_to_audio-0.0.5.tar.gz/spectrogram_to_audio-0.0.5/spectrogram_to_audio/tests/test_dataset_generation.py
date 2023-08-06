from unittest import TestCase
from unittest.mock import patch
import os

from config.load_config import config
from spectrogram_to_audio.data_preprocessing.dataset import get_dataset


class LoadDatasetTest(TestCase):

    @patch('spectrogram_to_audio.data_preprocessing.dataset.get_dataset_dir')
    def test_dataset_loading(self, mock1):

        def get_testing_dataset():
            relative_abs_path = os.path.dirname(__file__)
            mock1.return_value = "{}/audios/*.wav".format(relative_abs_path)
            return get_dataset(True)

        ds = get_testing_dataset()
        for spectrograms, audios in ds:
            assert(audios.shape == (config.AUDIO.SAMPLE_RATE * config.AUDIO.AUDIO_TIME_SEC, 1))
            assert(spectrograms.shape[-1] == config.SPECTROGRAM.SPEC_CHANNELS)
