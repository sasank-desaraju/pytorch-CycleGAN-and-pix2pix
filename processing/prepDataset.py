"""
Sasank Desaraju
7/27/2022
"""

"""
This takes images from the ModelData folder, performs a TTV split, and populates them into a pix2pix dataset folder.
"""

# TODO: Maybe, for the GNGNet comparison, we should not have any test images and use all our ICG data for training and validation so we can get the best model.

import csv
import os
import shutil
from math import floor

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# *** PARAMETERS ***


MODEL_NAME = "2024-08-24_Holdout"

VIS_SRC = "ModelData/" + MODEL_NAME + "/VIS/"
ICG_SRC = "ModelData/" + MODEL_NAME + "/ICG/"
VIS_DEST = "pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/A/"
ICG_DEST = "pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/B/"

TEST_FRAC = 0.2
VAL_FRAC = 0.2
TRAIN_FRAC = 1 - TEST_FRAC - VAL_FRAC


# *** END PARAMETERS ***


# Create the dataset folders if needed

if not os.path.isdir("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME):
    os.makedirs("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME)

if not os.path.isdir("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/A"):
    os.makedirs("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/A")

if not os.path.isdir(
    "pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/A/train"
):
    os.makedirs("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/A/train")

if not os.path.isdir("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/A/test"):
    os.makedirs("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/A/test")

if not os.path.isdir("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/A/val"):
    os.makedirs("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/A/val")

if not os.path.isdir("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/B"):
    os.makedirs("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/B")

if not os.path.isdir(
    "pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/B/train"
):
    os.makedirs("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/B/train")

if not os.path.isdir("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/B/test"):
    os.makedirs("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/B/test")

if not os.path.isdir("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/B/val"):
    os.makedirs("pytorch-CycleGAN-and-pix2pix/datasets/" + MODEL_NAME + "/B/val")


# Read in labels.csv

file_list = pd.read_csv("ModelData/" + MODEL_NAME + "/model_images.csv", header=None)

# Get TTV indices
num_samples = len(file_list)
# print(file_list)
# print(num_samples)
# print(file_list.iloc[0,0])
permutation = np.random.choice(a=num_samples, size=num_samples, replace=False)
test_list = permutation[0 : floor(TEST_FRAC * len(permutation))]
val_list = permutation[
    floor(TEST_FRAC * len(permutation)) : floor(
        (TEST_FRAC + VAL_FRAC) * len(permutation)
    )
]
train_list = permutation[
    floor((TEST_FRAC + VAL_FRAC) * len(permutation)) : len(permutation)
]  # Do I need a -1 at the end?


for idx in train_list:
    # print(list_of_rows[row])
    shutil.copyfile(
        os.path.join(VIS_SRC, file_list.iloc[idx, 0]),
        os.path.join(VIS_DEST + "train/", file_list.iloc[idx, 0]),
    )
    shutil.copyfile(
        os.path.join(ICG_SRC, file_list.iloc[idx, 0]),
        os.path.join(ICG_DEST + "train/", file_list.iloc[idx, 0]),
    )

for idx in test_list:
    # print(list_of_rows[row])
    shutil.copyfile(
        os.path.join(VIS_SRC, file_list.iloc[idx, 0]),
        os.path.join(VIS_DEST + "test/", file_list.iloc[idx, 0]),
    )
    shutil.copyfile(
        os.path.join(ICG_SRC, file_list.iloc[idx, 0]),
        os.path.join(ICG_DEST + "test/", file_list.iloc[idx, 0]),
    )

for idx in val_list:
    # print(list_of_rows[row])
    shutil.copyfile(
        os.path.join(VIS_SRC, file_list.iloc[idx, 0]),
        os.path.join(VIS_DEST + "val/", file_list.iloc[idx, 0]),
    )
    shutil.copyfile(
        os.path.join(ICG_SRC, file_list.iloc[idx, 0]),
        os.path.join(ICG_DEST + "val/", file_list.iloc[idx, 0]),
    )
