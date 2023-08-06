from data_preprocessing.dataset import get_dataset

train_dataset = get_dataset(True).batch(16)
validation_dataset = get_dataset(False).batch(16)

for spectrograms, audios in train_dataset.take(10):
    print(spectrograms.shape)
    print(audios.shape)
