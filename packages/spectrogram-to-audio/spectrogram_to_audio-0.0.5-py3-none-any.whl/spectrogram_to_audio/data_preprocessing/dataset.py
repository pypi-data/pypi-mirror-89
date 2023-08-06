import os
import tensorflow as tf
import tensorflow_io as tfio
import tensorflow_datasets as tfds
from tensorflow.data.experimental import AUTOTUNE

from config.load_config import config


@tf.function
def get_raw_audio(abs_file_path: tf.string) -> tf.Tensor:
    raw_audio = tf.io.read_file(abs_file_path)
    audio, sample_rate = tf.audio.decode_wav(raw_audio)
    return tf.reduce_mean(audio, axis=1)


@tf.function
def resize_audio(raw_audio: tf.Tensor) -> tf.Tensor:
    expected_audio_size = config.AUDIO.audio_time_sec * config.AUDIO.sample_rate
    audio_size = tf.size(raw_audio)
    if audio_size >= expected_audio_size:
        start = tf.random.uniform(
            shape=[1], minval=0, maxval=audio_size - expected_audio_size, dtype=tf.dtypes.int32
        )
        return tf.slice(raw_audio, start, [expected_audio_size])
    else:
        delt = expected_audio_size - audio_size
        return tf.pad(raw_audio, [[0, delt]], "CONSTANT")


@tf.function
def generate_mel_spectrogram(raw_audio: tf.Tensor) -> tf.Tensor:
    p = (config.SPECTROGRAM.FRAME_LENGTH - config.SPECTROGRAM.FRAME_STEP) // 2
    padded_raw_audio = tf.pad(
        raw_audio, [[p, p]], "REFLECT",
    )
    spectrogram = tf.math.abs(
        tf.signal.stft(
            padded_raw_audio,
            frame_length=config.SPECTROGRAM.FRAME_LENGTH,
            frame_step=config.SPECTROGRAM.FRAME_STEP,
            fft_length=config.SPECTROGRAM.FFT_LENGTH,
            window_fn=tf.signal.hann_window,
            pad_end=False,
        )
    )
    return tfio.experimental.audio.melscale(
        spectrogram,
        rate=config.AUDIO.SAMPLE_RATE,
        mels=config.SPECTROGRAM.SPEC_CHANNELS,
        fmin=config.SPECTROGRAM.FREQUENCY_MIN,
        fmax=config.SPECTROGRAM.FREQUENCY_MAX
    ), tf.expand_dims(raw_audio, axis=-1)


@tf.function
def unenumerate(ind: int, val: tf.Tensor) -> tf.Tensor:
    return val


def filter_train(is_train: bool):

    @tf.function
    def is_training(ind: int, val: tf.Tensor):
        return (ind % 8 != 0) == is_train

    return is_training


def download_dataset():
    dl_manager = tfds.download.DownloadManager(
        download_dir=config.DATASET.DATASET_LOCAL_PATH
    )
    return dl_manager.download_and_extract(
        config.DATASET.DATASET_URL
    )


def get_dataset_dir():
    dataset_path = download_dataset()
    path_to_audios = os.path.join(dataset_path, "LJSpeech-1.1/wavs/*.wav")
    return path_to_audios


def get_dataset(is_train: bool) -> tf.data.Dataset:
    return tf.data.Dataset.list_files(get_dataset_dir()) \
        .enumerate() \
        .filter(filter_train(is_train)) \
        .map(unenumerate, num_parallel_calls=AUTOTUNE) \
        .map(get_raw_audio, num_parallel_calls=AUTOTUNE) \
        .map(resize_audio, num_parallel_calls=AUTOTUNE) \
        .map(generate_mel_spectrogram, num_parallel_calls=AUTOTUNE)
