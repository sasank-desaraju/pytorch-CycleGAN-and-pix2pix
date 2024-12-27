"""
Sasank Desaraju
7/27/22
"""

"""
This takes raw images, a data CSV, model parameters (e.g. Dose, Timepoint), and a model name
and creates a folder in ModelData with image folders, a model-specific data CSV, and a readme.txt.
"""

import csv
import glob
import os

import cv2
import numpy as np
import pandas as pd
from PIL import Image

# setupModel(INFO_CSV, DOSE, TIME, RAW_IMAGE_DIR, MODEL_NAME)
# setupModel('Dose and Dissection Timepoint for AI.csv', -1, -1, 'Raw Images/', 'BothDose_9_30')

MODEL_NAME = "2024_11_24_Older_BothDose"
DOSE = -1
TIME = -1
INFO_CSV = "/blue/azarrinpar/ICG_AI/Dose and Dissection Timepoint for AI.csv"
# RAW_IMAGE_DIR = "Images/"
IMAGE_RESAMPLE_SIZE = (
    460,
    360,
)  # Our ICG images are WxH=460x360 but we want to resize them to 640x360 for the Madani collaboration
# We will use PIL.Image.resize() to resize the images to this size

# ? Do these actually get used? OUTPUT_DIR is used in makeCSV, but this does not get called in the main function.
# OUTPUT_DIR = "~/UFL Dropbox/Sasank Desaraju/ICG Study/data/"
# OUTPUT_DIR = "/mnt/Linux-Storage/Dropbox (UFL)/ICG Study/data/"
CSV_NAME = "2024_11_24_older_both_dose"
RAW_IMAGE_DIR = "Images/"
PROC_IMAGE_DIR = "/blue/azarrinpar/ICG_AI/pytorch-CycleGAN-and-pix2pix/img_src/2024_11_24/Images/"
# PROC_IMAGE_DIR = "/blue/azarrinpar/ICG_AI/Proc_Images/"
# PROC_IMAGE_DIR = "/mnt/Linux-Storage/Dropbox (UFL)/ICG Study/Images/"
VIS_DIR = "/blue/azarrinpar/ICG_AI/pytorch-CycleGAN-and-pix2pix/img_src/2024_11_24/vis/"
# VIS_DIR = "~/UFL Dropbox/Sasank Desaraju/ICG Study/vis/"
# VIS_DIR = "/mnt/Linux-Storage/Dropbox (UFL)/ICG Study/vis/"
ICG_DIR = "/blue/azarrinpar/ICG_AI/pytorch-CycleGAN-and-pix2pix/img_src/2024_11_24/icg/"
# ICG_DIR = "~/UFL Dropbox/Sasank Desaraju/ICG Study/icg/"
# ICG_DIR = "/mnt/Linux-Storage/Dropbox (UFL)/ICG Study/icg/"
# IMAGE_DIR = "~/UFL Dropbox/Sasank Desaraju/ICG Study/Images/"
IMAGE_DIR = "/blue/azarrinpar/ICG_AI/pytorch-CycleGAN-and-pix2pix/img_src/2024_11_24/Images/"
# IMAGE_DIR = "/mnt/Linux-Storage/Dropbox (UFL)/ICG Study/Images/"

# Read image
# image = cv2.imread("/HDD_Linux/Dropbox (UFL)/ICG Study/Raw Images/P16S5.png")
# cv2.imwrite('visual_test.png', image)
# cv2.imwrite('visual_test.png', visual_image)
# cv2.imwrite('ICG_test.png', ICG_image)


# visual_image = image[2 : 362, 0 : 460]
# ICG_image = image[362: 722, 0 : 460]

"""
setupModel is the most important function in this file. It takes the following parameters:
INFO_CSV - the CSV with the patient info
DOSE - the dose of ICG used in the images
TIME - the timepoint of the images
RAW_IMAGE_DIR - the directory with the raw images
MODEL_NAME - the name of the model

It creates a folder in ModelData with image folders, a model-specific data CSV, and a readme.txt.
Inside the function, it calls compareLists, createMergedCSV, and processRaw.
- compareLists prints out the files that are in one list but not the other.
This is to check that the images and the CSV are the same.
- createMergedCSV creates a CSV with only the images that fit the criteria.
- processRaw processes the images in the raw image folder and puts them in the model folder.
processRaw is the file that is modified when resizing the images to the GNGNet size for the Madani collaboration.
"""


def setupModel(INFO_CSV, DOSE, TIME, RAW_IMAGE_DIR, MODEL_NAME):

    compareLists(
        INFO_CSV, RAW_IMAGE_DIR
    )  # - just print whatever is not in both INFO_CSV && RAW_IMAGE_DIR

    # createFolder - warn if folder is not empty. Name it MODEL_NAME
    if os.path.isdir("ModelData/" + MODEL_NAME):
        print("Warning: A folder named %s exists already" % MODEL_NAME)
    else:
        os.makedirs("ModelData/" + MODEL_NAME)

    # Why is this Images folder created? Seems to not be used.
    if os.path.isdir("ModelData/" + MODEL_NAME + "/Images"):
        print("Warning: The image folder in %s exists already" % MODEL_NAME)
    else:
        os.makedirs("ModelData/" + MODEL_NAME + "/Images")

    # in the folder, write a txt with INFO_CSV, DOSE, etc. for notekeeping
    with open("ModelData/" + MODEL_NAME + "/readme.txt", "w") as f:
        f.write("INFO_CSV = " + INFO_CSV + "\n")
        f.write("DOSE = " + str(DOSE) + "\n")
        f.write("TIME = " + str(TIME) + "\n")
        f.write("RAW_IMAGE_DIR = " + RAW_IMAGE_DIR + "\n")
        f.write("MODEL_NAME = " + MODEL_NAME + "\n")
        f.write("IMAGE_RESAMPLE_SIZE = " + str(IMAGE_RESAMPLE_SIZE) + "\n")

    # - write only those which fit all criteria
    createMergedCSV(INFO_CSV, DOSE, TIME, RAW_IMAGE_DIR, MODEL_NAME)

    # - process all from raw image folder to folder in model directory
    processRaw(RAW_IMAGE_DIR, MODEL_NAME)
    # this ^ should work in this series because it just checked that the images were in
    # the raw image dir during the merged CSV creation
    return


def compareLists(INFO_CSV, RAW_IMAGE_DIR):
    info_data = pd.read_csv(INFO_CSV)
    info_list = sorted(info_data["Patient"])
    # print(info_list)

    image_list = sorted(os.listdir(RAW_IMAGE_DIR))
    # print(image_list)

    # have this print out what files are different if I can
    if info_list != image_list:
        print("Raw image directory files and info CSV files are not the same!")
        print(
            "The files only in the CSV are "
            + str(sorted(list(set(info_list) - set(image_list))))
        )
        print(
            "The files only in the raw images are "
            + str(sorted(list(set(image_list) - set(info_list))))
        )
        # I could also define their sets and use [set].symmetric_difference([other set])


def createMergedCSV(INFO_CSV, DOSE, TIME, RAW_IMAGE_DIR, MODEL_NAME):
    info_data = pd.read_csv(INFO_CSV)
    info_set = set(info_data["Patient"])
    image_set = set(os.listdir(RAW_IMAGE_DIR))
    inter_list = sorted(info_set.intersection(image_set))

    model_images = []
    for file in inter_list:
        try:
            index = pd.Index(info_data["Patient"]).get_loc(file)
        except ValueError:
            print("The file " + file + " is not in the info CSV.")
        if (DOSE == -1 or info_data.iloc[index, 1] == DOSE) and (
            TIME == -1 or info_data.iloc[index, 2] == TIME
        ):
            model_images.append(file)
    image_row = zip(model_images)
    # print(model_images)

    with open("ModelData/" + MODEL_NAME + "/model_images.csv", "w") as f:
        writer = csv.writer(f, lineterminator="\n")
        for row in image_row:
            writer.writerow(row)
            # print("Printed row %s" % row)


def processRaw(RAW_IMAGE_DIR, MODEL_NAME):
    image_list = pd.read_csv(
        "ModelData/" + MODEL_NAME + "/model_images.csv", header=None
    )
    # print(type(image_list))
    # print(image_list.iloc[:,0])
    if os.path.isdir("ModelData/" + MODEL_NAME + "/VIS"):
        print("Warning: A visual image folder for %s exists already" % MODEL_NAME)
    else:
        os.makedirs("ModelData/" + MODEL_NAME + "/VIS")
    if os.path.isdir("ModelData/" + MODEL_NAME + "/ICG"):
        print("Warning: A ICG image folder for %s exists already" % MODEL_NAME)
    else:
        os.makedirs("ModelData/" + MODEL_NAME + "/ICG")
    i = 0
    for image_file in image_list.iloc[:, 0]:
        print(image_file)
        if image_file.endswith(".png"):
            # print(image_file)
            try:
                image = cv2.imread(RAW_IMAGE_DIR + image_file)
            except FileNotFoundError:
                print("File %s was not found in the RAW_IMAGE_DIR" % image_file)
            visual_image = image[2:362, 0:460]
            ICG_image = image[362:722, 0:460]

            # Resize and resample using cv2
            visual_image = cv2.resize(
                visual_image,
                (IMAGE_RESAMPLE_SIZE[0], IMAGE_RESAMPLE_SIZE[1]),
                interpolation=cv2.INTER_NEAREST,
            )
            ICG_image = cv2.resize(
                ICG_image,
                (IMAGE_RESAMPLE_SIZE[0], IMAGE_RESAMPLE_SIZE[1]),
                interpolation=cv2.INTER_NEAREST,
            )

            """
            # Image resampling code using PIL
            visual_image = Image.fromarray(visual_image)
            visual_image = visual_image.resize(
                (IMAGE_RESAMPLE_SIZE[0], IMAGE_RESAMPLE_SIZE[1]),
                Image.Resampling.NEAREST,
            )
            visual_image = np.array(visual_image)
            # Assert that the image is a numpy array
            assert type(visual_image) == np.ndarray
            # Print the shape of the image
            print(visual_image.shape)

            ICG_image = Image.fromarray(ICG_image)
            ICG_image = ICG_image.resize(
                (IMAGE_RESAMPLE_SIZE[0], IMAGE_RESAMPLE_SIZE[1]),
                # Image.Resampling.NEAREST,
            )
            ICG_image = np.array(ICG_image)
            # Assert that the image is a numpy array
            assert type(ICG_image) == np.ndarray
            """

            # cv2.imwrite(PROC_IMAGE_DIR + 'vis_' + str(i) + '.png', visual_image)
            # cv2.imwrite(PROC_IMAGE_DIR + 'ICG_' + str(i) + '.png', ICG_image)

            # cv2.imwrite('ModelData/' + MODEL_NAME + '/VIS/' + 'vis_' + str(i) + '_' + image_file, visual_image)
            # Create random numpy array for testing
            # test_image = np.random.randint(0, 255, (640, 360, 3), dtype=np.uint8)
            # print("Test image created")
            # cv2.imwrite("ModelData/" + MODEL_NAME + "/VIS/" + "test_image.png", test_image)
            # print("Test image saved")
            cv2.imwrite("ModelData/" + MODEL_NAME + "/VIS/" + image_file, visual_image)

            # cv2.imwrite('ModelData/' + MODEL_NAME + '/ICG/' + 'icg_' + str(i) + '_' + image_file, ICG_image)
            cv2.imwrite("ModelData/" + MODEL_NAME + "/ICG/" + image_file, ICG_image)
            i += 1
            # print("test")


def makeCSV(IMAGE_DIR, OUTPUT_DIR, CSV_NAME):
    # print(glob.glob1(IMAGE_DIR, "grid*.tif"))
    vis = np.array(glob.glob1(IMAGE_DIR, "vis*.png"))
    vis = np.insert(sorted(vis), [0], ["vis"])
    icg = np.array(glob.glob1(IMAGE_DIR, "ICG*.png"))
    icg = np.insert(sorted(icg), [0], ["icg"])
    # print(grid)

    vis_and_icg = np.concatenate((vis[:, None], icg[:, None]), axis=1)
    headers = np.array([["vis", "icg"]])
    np.savetxt(OUTPUT_DIR + CSV_NAME + ".csv", vis_and_icg, fmt="%s", delimiter=",")


def pruneCSV(CSV_NAME, KEY_CSV_NAME, DOSE=-1, TIME=-1):
    # This will work by adding to a blank CSV only the intersect between the data_csv
    # and the favored elements of the key_csv.

    # create writer for final data_csv

    # loop through key_csv
    # if key.dose[i] == DOSE && key.time[i] == time && grep(key[i] in data_csv)
    # then write that name to the new csv

    # assign this new csv the name of CSV_NAME
    return  # remove this later lol


# makeCSV(IMAGE_DIR, OUTPUT_DIR, CSV_NAME)
# processRaw(RAW_IMAGE_DIR)
# info_data = pd.read_csv(INFO_CSV)
# info_list = sorted(info_data['Patient'])
# print(info_list)
# compareLists(INFO_CSV, RAW_IMAGE_DIR)

if __name__ == "__main__":
    # setupModel(INFO_CSV, DOSE, TIME, RAW_IMAGE_DIR, MODEL_NAME)
    setupModel(
        INFO_CSV=INFO_CSV,
        DOSE=DOSE,
        TIME=TIME,
        RAW_IMAGE_DIR=RAW_IMAGE_DIR,
        MODEL_NAME=MODEL_NAME,
    )

# Display cropped image
"""
cv2.imwrite('visual_test.png', visual_image)
cv2.imwrite('ICG_test.png', ICG_image)
cv2.imshow("Cropped image", visual_image)
cv2.waitKey(0)
"""
