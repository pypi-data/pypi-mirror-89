import tensorflow as tf
from typing import Tuple, List
import os
from dynaconf import settings

# configuration
TRAIN_SPLIT_RATE = settings.TRAIN_SPLIT_RATE
VAL_SPLIT_RATE = settings.VAL_SPLIT_RATE

# constants
TEST_SPLIT_RATE = 1 - TRAIN_SPLIT_RATE - VAL_SPLIT_RATE
FILES_DS = Tuple[List[str], int,
                 Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]]
FILES_TEST = Tuple[List[str], int, tf.data.Dataset]


def download_data(ds_name: str, subdir: str, ds_origin: str) -> None:
    tf.keras.utils.get_file(
        ds_name,
        origin='/'.join([ds_origin, ds_name]),
        extract=True,
        cache_dir='.', cache_subdir=subdir
    )


def get_filenames(data_dir: str) -> List[str]:
    filenames = tf.io.gfile.glob(os.path.join(data_dir, '*', '*.wav'))
    return tf.random.shuffle(filenames)


def prepare_one_dataset(data_dir: str) -> FILES_TEST:
    filenames = get_filenames(data_dir)
    ds_commands = [dir_name
                   for dir_name in tf.io.gfile.listdir(data_dir)
                   if os.path.isdir(os.path.join(data_dir, dir_name))]
    num_samples = len(filenames)
    return (ds_commands, num_samples,
            tf.data.Dataset.from_tensor_slices(filenames))


def prepare_dataset(data_dir: str) -> FILES_DS:
    filenames = get_filenames(data_dir)
    ds_commands = [dir_name
                   for dir_name in tf.io.gfile.listdir(data_dir)
                   if os.path.isdir(os.path.join(data_dir, dir_name))]
    num_samples = len(filenames)
    num_train = int(TRAIN_SPLIT_RATE * num_samples)
    num_val = int(VAL_SPLIT_RATE * num_samples)
    train_files = filenames[:num_train]
    val_files = filenames[num_train:num_train + num_val]
    test_files = filenames[num_train + num_val:]
    return (ds_commands, num_train,
            (tf.data.Dataset.from_tensor_slices(train_files),
             tf.data.Dataset.from_tensor_slices(val_files),
             tf.data.Dataset.from_tensor_slices(test_files))
            )
