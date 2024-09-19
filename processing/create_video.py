"""
Sasank Desaraju
11/10/2022

Let's make some videos!!!
"""

from moviepy.editor import ImageSequenceClip
import glob

files = sorted(glob.glob('CreatedVideos/Frames/*.png'))
files = files[:300]
#print(files)

clip = ImageSequenceClip(files, fps=30)
#clip.write_videofile('CreatedVideos/VideoWithCaption_new.mp4', fps=30)
clip.write_gif('CreatedVideos/AI_Gif_shorter.gif')