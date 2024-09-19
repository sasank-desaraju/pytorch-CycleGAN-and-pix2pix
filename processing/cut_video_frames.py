"""
Sasank Desaraju
11/10/2022

This is to cut the video frames into VIS and ICG and just the size we want.py
"""

import cv2
import os
import numpy as np
import pandas as pd

RAW_IMAGE_DIR = '/media/sasank/LinuxStorage/Dropbox (UFL)/ICG Study/RawVideoClips/TriView_8/'
OUTPUT_DIR = '/media/sasank/LinuxStorage/Dropbox (UFL)/ICG Study/ProcessedVideoClips/ICG16_TriView_8/'

def processRaw(RAW_IMAGE_DIR, OUTPUT_DIR):
    #print(type(image_list))
    #print(image_list.iloc[:,0])
    if not os.path.isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print("Created folder %s" % OUTPUT_DIR)
    if not os.path.isdir(OUTPUT_DIR + 'VIS/'):
        os.makedirs(OUTPUT_DIR + 'VIS/')
        print("Created VIS folder %s" % (OUTPUT_DIR + 'VIS/'))
    VIS_DIR = OUTPUT_DIR + 'VIS/'
    if not os.path.isdir(OUTPUT_DIR + 'ICG/'):
        os.makedirs(OUTPUT_DIR + 'ICG/')
        print("Created ICG folder %s" % (OUTPUT_DIR + 'ICG/'))
    ICG_DIR = OUTPUT_DIR + 'ICG/'
    i = 0       # What's this counter for? Seems useless...
    for image_file in sorted(os.walk(RAW_IMAGE_DIR))[0][2]:
        #print(image_file)
        if image_file.endswith(".jpg"):
            #print(image_file)
            try:
                image = cv2.imread(RAW_IMAGE_DIR + image_file)
            except:
                print("File %s cannot be parsed as image." % image_file)
            visual_image = image[2 : 362, 0 : 460]
            ICG_image = image[362: 722, 0 : 460]

            #cv2.imwrite(PROC_IMAGE_DIR + 'vis_' + str(i) + '.png', visual_image)
            #cv2.imwrite(PROC_IMAGE_DIR + 'ICG_' + str(i) + '.png', ICG_image)

            #cv2.imwrite('ModelData/' + MODEL_NAME + '/VIS/' + 'vis_' + str(i) + '_' + image_file, visual_image)
            cv2.imwrite(VIS_DIR + image_file, visual_image)
            #cv2.imwrite('ModelData/' + MODEL_NAME + '/ICG/' + 'icg_' + str(i) + '_' + image_file, ICG_image)
            cv2.imwrite(ICG_DIR + image_file, ICG_image)
            i += 1      # What's this counter for? Seems useless...


processRaw(RAW_IMAGE_DIR, OUTPUT_DIR)