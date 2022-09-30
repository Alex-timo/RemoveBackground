import os
import numpy as np
import argparse
import cv2

import moviepy.video.io.ImageSequenceClip
from PIL import Image, ImageFile
import segment_functions as seg
ImageFile.LOAD_TRUNCATED_IMAGES = True


def split_video(videopath, framepath, videoname):
    seg.create_dir(framepath)
    # parse all args
    # parser = argparse.ArgumentParser()
    # parser.add_argument('source', type=str, help='Path to source video')
    # parser.add_argument('dest_folder', type=str, help='Path to destination folder')
    # args = parser.parse_args()

    # get file path for desired video and where to save frames locally
    # cap = cv2.VideoCapture(args.source)
    # path_to_save = os.path.abspath(args.dest_folder)
    cap = cv2.VideoCapture(videopath + "/" + videoname)
    path_to_save = os.path.abspath(framepath)

    current_frame = 1

    if (cap.isOpened() == False):
        print('Cap is not open')

    # cap opened successfully
    while (cap.isOpened()):

        # capture each frame
        ret, frame = cap.read()
        if (ret == True):

            # Save frame as a jpg file
            name = 'frame' + str(current_frame) + '.png'
            print(f'Creating: {name}')
            cv2.imwrite(os.path.join(path_to_save, name), frame)

            # keep track of how many images you end up with
            current_frame += 1

        else:
            break

    # release capture
    cap.release()
    print('done')


def make_video(videopath, framepath, videoname , numOfFrames):
    seg.create_dir(videopath)
    seg.create_dir(framepath)
    image_files = []

    for img_number in range(1, numOfFrames):
        # image_files.append(path_to_images + 'image_folder/image_' + str(img_number) + '.png')
        image_files.append(framepath + '/frame' + str(img_number) + '.png')

    fps = 30

    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
    # clip.write_videofile(path_to_videos + 'my_new_video.mp4')
    clip.write_videofile(videopath + "/" + videoname)
