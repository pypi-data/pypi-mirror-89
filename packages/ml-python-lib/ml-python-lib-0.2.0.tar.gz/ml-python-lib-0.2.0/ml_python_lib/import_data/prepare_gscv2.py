import tensorflow as tf
from typing import Tuple, List
import os
import numpy as np
from pydub import AudioSegment
from pydub.utils import make_chunks

FILES_DS = Tuple[int,
                 Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]]

ALL_DS = Tuple[int, tf.data.Dataset]


# avoid load original background noise data
def get_all_filenames(data_dir: str) -> List[str]:
    filenames = tf.io.gfile.glob(os.path.join(data_dir, '[a-z]*', '*.wav'))
    return filenames


# split these noise data to 1 seconds clips
def split_noise(subdir_train: str) -> None:
    new_dir = os.path.join(subdir_train, 'background_noise')
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
        background_noise_files = tf.io.gfile.glob(
            os.path.join(subdir_train, '_background_noise_', '*.wav'))
        for noise in background_noise_files:
            my_audio = AudioSegment.from_file(noise, "wav")
            chunk_length_ms = 1000
            chunks = make_chunks(my_audio, chunk_length_ms)
            chunks = chunks[:-2]
            for i, chunk in enumerate(chunks):
                chunk_name = "chunk{0}_{1}".format(i, os.path.basename(noise))
                export_path = \
                    os.path.join(subdir_train, 'background_noise', chunk_name)
                chunk.export(export_path, format="wav", cover=noise)
        print("finish splitting noise into 1 seconds clips")
    else:
        print("already split")


# load dataset according to the txt file
def prepare_gsc_dataset(subdir_train: str) -> FILES_DS:
    test_files = np.loadtxt(
        fname=os.path.join(
            subdir_train, 'testing_list.txt'), delimiter=' ', dtype=str)
    test_files = [os.path.join(subdir_train, f)for f in test_files]
    val_files = np.loadtxt(
        fname=os.path.join(
            subdir_train, 'validation_list.txt'), delimiter=' ', dtype=str)
    val_files = [os.path.join(subdir_train, f)for f in val_files]
    all_ds = get_all_filenames(subdir_train)
    train_files = list(set(all_ds)-set(test_files)-set(val_files))
    # because we have few noise so we reuse it.
    noise = tf.io.gfile.glob(
        os.path.join(subdir_train, 'background_noise', '*.wav'))
    for i in range(3):
        train_files += noise
    val_files += noise
    num_train = len(train_files)
    return (num_train,
            (tf.data.Dataset.from_tensor_slices(
                tf.random.shuffle(train_files)),
             tf.data.Dataset.from_tensor_slices(tf.random.shuffle(val_files)),
             tf.data.Dataset.from_tensor_slices(test_files))
            )


# get the dataset class
def get_ds_class(task: str,):
    allowed_tasks = ['12cmd', '35word']
    if task == '12cmd':
        # standard the paper asked
        ds_class = tf.lookup.StaticHashTable(
            initializer=tf.lookup.KeyValueTensorInitializer(
                keys=tf.constant(['unknown', '_unknown_', '_silence_',
                                  'background_noise',
                                  'yes', 'no', 'up', 'down',
                                  'left', 'right', 'on', 'off', 'stop', 'go']),
                values=tf.constant(
                    [0, 0, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
            ),
            default_value=tf.constant(0)
        )
        num_class = 12
    elif task == '35word':
        # 35words
        ds_class = tf.lookup.StaticHashTable(
            initializer=tf.lookup.KeyValueTensorInitializer(
                keys=tf.constant(['unknown',
                                  'background_noise',
                                  'yes', 'no', 'up', 'down',
                                  'left', 'right', 'on',
                                  'off', 'stop', 'go', 'backward',
                                  'bed', 'bird', 'cat',
                                  'dog', 'eight', 'five', 'follow',
                                  'forward', 'four', 'happy',
                                  'house', 'learn', 'marvin',
                                  'nine', 'one', 'seven',
                                  'sheila', 'six', 'three', 'tree',
                                  'two', 'visual', 'wow', 'zero']),
                values=tf.constant([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                    13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                    23, 24, 25, 26, 27, 28, 29, 30, 31,
                                    32, 33, 34, 35, 36]),
            ),
            default_value=tf.constant(0)
        )
        num_class = 37
    else:
        raise Exception('Task must be one of: {}'.format(allowed_tasks))
    return num_class, ds_class


# get all train dataset
def train_all(subdir_train: str) -> ALL_DS:
    train_ds = get_all_filenames(subdir_train)
    num_train = len(train_ds)
    train_ds = tf.random.shuffle(train_ds)
    train_ds = tf.data.Dataset.from_tensor_slices(train_ds)
    return num_train, train_ds
