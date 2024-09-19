"""
Sasank Desaraju
11/10/2022

Create video frames from ICG model outputs.
"""

#from moviepy.editor import ImageSequenceClip
import glob
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np

VIS_files = sorted(glob.glob('pytorch-CycleGAN-and-pix2pix/results/HighDose_10_19/test_latest/images/*real_A.png'))
ICG_real_files = sorted(glob.glob('pytorch-CycleGAN-and-pix2pix/results/HighDose_10_19/test_latest/images/*real_B.png'))
ICG_synthetic_files = sorted(glob.glob('pytorch-CycleGAN-and-pix2pix/results/HighDose_10_19/test_latest/images/*fake_B.png'))
SAVE_DIR = 'CreatedVideos/Frames/'

VIS_frames = [None] * len(VIS_files)
ICG_real_frames = [None] * len(VIS_files)
ICG_synthetic_frames = [None] * len(VIS_files)
real_video_frames = [None] * len(VIS_files)
synthetic_video_frames = [None] * len(VIS_files)
bruh_frames = [None] * len(VIS_files)
CAPTION_HEIGHT = 75

for idx, element in enumerate(VIS_files):
    VIS_matrix = (0.7,0,0,0, 0,0.7,0,0, 0,0,0.7,0)
    ICG_matrix = (0.0,0,0,0, 0,0.8,0,0, 0,0,0.0,0)

    VIS_frames[idx] = Image.open(VIS_files[idx]).convert('RGB')
    VIS_frames[idx] = VIS_frames[idx].convert('RGB', VIS_matrix)
    VIS_array = np.array(VIS_frames[idx])

    ICG_real_frames[idx] = Image.open(ICG_real_files[idx]).convert('RGB')
    ICG_real_frames[idx] = ICG_real_frames[idx].convert('RGB', ICG_matrix)
    ICG_real_array = np.array(ICG_real_frames[idx])

    ICG_synthetic_frames[idx] = Image.open(ICG_synthetic_files[idx]).convert('RGB')
    ICG_synthetic_frames[idx] = ICG_synthetic_frames[idx].convert('RGB', ICG_matrix)
    ICG_synthetic_array = np.array(ICG_synthetic_frames[idx])

    real_bruh = np.zeros_like(VIS_array)
    for index in np.ndindex(real_bruh.shape):
        if int(VIS_array[index]) + int(ICG_real_array[index]) > 255:
            real_bruh[index] = 255
        else:
            real_bruh[index] = VIS_array[index] + ICG_real_array[index]

    #print(idx)
    #synthetic_bruh = VIS_array + ICG_synthetic_array
    synthetic_bruh = np.zeros_like(VIS_array)
    for index in np.ndindex(synthetic_bruh.shape):
        if int(VIS_array[index]) + int(ICG_synthetic_array[index]) > 255:
            synthetic_bruh[index] = 255
        else:
            synthetic_bruh[index] = VIS_array[index] + ICG_synthetic_array[index]

    print(idx)

    both_bruh = np.concatenate((real_bruh, synthetic_bruh), axis=1)
    #print(np.shape(real_bruh))
    height, width, channels = np.shape(both_bruh)
    caption = np.full((CAPTION_HEIGHT, width, channels), 255, dtype=np.uint8)
    both_bruh = np.concatenate((both_bruh, caption), axis=0)
    #print(height, width, channels)
    #if idx == 5:
    #    break
    bruh_frames[idx] = Image.fromarray(both_bruh)
    caption_text = ImageDraw.Draw(bruh_frames[idx])
    myFont = ImageFont.truetype("arial.ttf", 20)
    caption_text.text((15 + 0, 265), "Ground truth ICG (green)", font=myFont, fill=(0,0,0))
    caption_text.text((15 + 5, 265 + 30), "overlaid on visual image", font=myFont, fill=(0,0,0))
    caption_text.text((275 + 5, 265), "Synthetic ICG (green)", font=myFont, fill=(0,0,0))
    caption_text.text((275, 265 + 30), "overlaid on visual image", font=myFont, fill=(0,0,0))


for idx, image in enumerate(bruh_frames):
    image.save(SAVE_DIR + 'frame%04d.png' % idx)




#files = sorted(glob.glob('pytorch-CycleGAN-and-pix2pix/results/HighDose_10_19/test_latest/images/*fake_B.png'))