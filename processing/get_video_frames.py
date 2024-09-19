from moviepy.editor import VideoFileClip
import numpy as np
import os
from datetime import timedelta

INPUT_FILE = '/media/sasank/LinuxStorage/Dropbox (UFL)/ICG Study/ICG16.mp4'
OUTPUT_DIR = '/media/sasank/LinuxStorage/Dropbox (UFL)/ICG Study/RawVideoClips/TriView_X'
FRAME_START = 41890
FRAME_END = 42933

SAVING_FRAMES_PER_SECOND = 30

def format_timedelta(td):
    """Utility function to format timedelta objects in a cool way (e.g 00:00:20.05) 
    omitting microseconds and retaining milliseconds"""
    result = str(td)
    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")
    ms = int(ms)
    ms = round(ms / 1e4)
    return f"{result}.{ms:02}".replace(":", "-")

def main(video_file):
    # load the video clip
    video_clip = VideoFileClip(video_file)
    # make a folder by the name of the video file
    #filename, _ = os.path.splitext(video_file)
    #filename += "-moviepy"
    #filename = '/media/sasank/LinuxStorage/Dropbox (UFL)/ICG Study/Videos/TriView_1'
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    # if the SAVING_FRAMES_PER_SECOND is above video FPS, then set it to FPS (as maximum)
    saving_frames_per_second = min(video_clip.fps, SAVING_FRAMES_PER_SECOND)
    # if SAVING_FRAMES_PER_SECOND is set to 0, step is 1/fps, else 1/SAVING_FRAMES_PER_SECOND
    step = 1 / video_clip.fps if saving_frames_per_second == 0 else 1 / saving_frames_per_second
    # iterate over each possible frame
    for current_duration in np.arange(FRAME_START * step, FRAME_END * step, step):
        # format the file name and save it
        frame_duration_formatted = format_timedelta(timedelta(seconds=current_duration)).replace(":", "-")
        frame_filename = os.path.join(OUTPUT_DIR, f"frame{frame_duration_formatted}.jpg")
        # save the frame with the current duration
        video_clip.save_frame(frame_filename, current_duration)

if __name__ == "__main__":
    import sys
    #video_file = sys.argv[1]
    #video_file = '/media/sasank/LinuxStorage/Dropbox (UFL)/ICG Study/ICG16.mp4'
    main(INPUT_FILE)