# This is a sample Python script.
import os

import segment_functions as seg
import shutil
import fnmatch
import video_functions as video_funcs
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for filename in os.scandir("images"):
        if filename.is_file():
            if ".png" not in filename.name:
                print("Only PNG format allowed in images folder, choose different files.")
                exit()
    for filename in os.scandir("original_video"):
        if filename.is_file():
            if ".mp4" not in filename.name:
                print("Only MP4 format allowed in original_vidoe folder, choose different files.")
                exit()
    print("1 - change image background to one color")
    print("2 - change video background to one color")
    print("3 - add custom background to image")
    print("4 - add custom background to video")
    print("5 - count people in image")
    print("6 - count people in video")
    #op_choice = int(input("choose operation (enter the relevant number): "))
    bool_num = True
    op_choice = 0
    try:
        op_choice = int(input("choose operation (enter the relevant number): "))
    except:
        bool_num = False

    while bool_num is False or (op_choice > 9 or op_choice < 1):
        try:
            op_choice = int(input("choose operation (enter the relevant number): "))
            bool_num = True
        except:
            bool_num = False

    if op_choice == 1:
        print("1 - white")
        print("2 - blue")
        print("3 - light green")
        print("4 - red")
        print("5 - black")
        print("6 - cyan")
        print("7 - light purple")
        print("8 - yellow")
        print("9 - transparent")

        if os.path.isdir("changed_images"):
            shutil.rmtree('changed_images')
        bool_color = True
        color_choice = 0
        try:
            color_choice = int(input("choose color (enter the relevant number): "))
        except:
            bool_color = False

        while bool_color is False or (color_choice > 9 or color_choice < 1):
            try:
                color_choice = int(input("choose color (enter the relevant number): "))
                bool_color = True
            except:
                bool_color = False
        seg.segmentation("images", "changed_images", color_choice)
        if color_choice == 9:
            for filename in os.scandir("changed_images"):
                if filename.is_file():
                    print(filename.name)
                    seg.convertImage("changed_images", "changed_images", filename.name)

    if op_choice == 2:
        if os.path.isdir("original_frames"):
            shutil.rmtree('original_frames')
        if os.path.isdir("new_frames"):
            shutil.rmtree('new_frames')
        if os.path.isdir("new_video"):
            shutil.rmtree('new_video')
        for filename in os.scandir("original_video"):
            if filename.is_file():
                video_funcs.split_video("original_video", "original_frames", filename.name)
                break

        print("1 - white")
        print("2 - blue")
        print("3 - light green")
        print("4 - red")
        print("5 - black")
        print("6 - cyan")
        print("7 - light purple")
        print("8 - yellow")
        print("9 - transparent")
        bool_color = True
        color_choice = 0
        try:
            color_choice = int(input("choose color (enter the relevant number): "))
        except:
            bool_color = False

        while bool_color is False or (color_choice > 9 or color_choice < 1):
            try:
                color_choice = int(input("choose color (enter the relevant number): "))
                bool_color = True
            except:
                bool_color = False

        seg.segmentation("original_frames", "new_frames", color_choice)
        if color_choice == 9:
            for filename in os.scandir("new_frames"):
                if filename.is_file():
                    print(filename.name)
                    seg.convertImage("new_frames", "new_frames", filename.name)

        frame_count = 0
        for filename in os.scandir("new_frames"):
            if filename.is_file():
                frame_count += 1

        video_funcs.make_video("new_video", "new_frames", "test.mp4", frame_count)

    if op_choice == 3:
        if os.path.isdir("changed_images"):
            shutil.rmtree('changed_images')
        background_image = ""
        for filename in os.scandir("custom_background"):
            if filename.is_file():
                print(filename.name)
                background_image = filename.name
                break

        seg.segmentation("images", "changed_images", 1)
        for filename in os.scandir("changed_images"):
            if filename.is_file():
                print(filename.name)
                seg.convertImage("changed_images", "changed_images", filename.name)
                seg.overlay("changed_images", "custom_background", "changed_images", background_image, filename.name)

    if op_choice == 4:
        background_image = ""
        for filename in os.scandir("custom_background"):
            if filename.is_file():
                print(filename.name)
                background_image = filename.name
                break

        if os.path.isdir("original_frames"):
            shutil.rmtree('original_frames')
        if os.path.isdir("new_frames"):
            shutil.rmtree('new_frames')
        if os.path.isdir("new_video"):
            shutil.rmtree('new_video')
        for filename in os.scandir("original_video"):
            if filename.is_file():
                video_funcs.split_video("original_video", "original_frames", filename.name)
                break

        seg.segmentation("original_frames", "new_frames", 1)
        for filename in os.scandir("new_frames"):
            if filename.is_file():
                print(filename.name)
                seg.convertImage("new_frames", "new_frames", filename.name)
                seg.overlay("new_frames", "custom_background", "new_frames", background_image, filename.name)

        frame_count = 0
        for filename in os.scandir("new_frames"):
            if filename.is_file():
                frame_count += 1

        video_funcs.make_video("new_video", "new_frames", "test.mp4", frame_count)

    if op_choice == 5:
        if os.path.isdir("changed_images"):
            shutil.rmtree('changed_images')
        seg.black_white_segmentation("images", "changed_images")
        for filename in os.scandir("changed_images"):
            if filename.is_file():
                print(filename.name)
                seg.get_contours("changed_images", "changed_images", "images", filename.name)

    if op_choice == 6:
        if os.path.isdir("original_frames"):
            shutil.rmtree('original_frames')
        if os.path.isdir("new_frames"):
            shutil.rmtree('new_frames')
        if os.path.isdir("new_video"):
            shutil.rmtree('new_video')
        for filename in os.scandir("original_video"):
            if filename.is_file():
                video_funcs.split_video("original_video", "original_frames", filename.name)
                break

        seg.black_white_segmentation("original_frames", "new_frames")
        for filename in os.scandir("new_frames"):
            if filename.is_file():
                print(filename.name)
                seg.get_contours("new_frames", "new_frames", "original_frames", filename.name)

        frame_count = 0
        for filename in os.scandir("new_frames"):
            if filename.is_file():
                frame_count += 1

        video_funcs.make_video("new_video", "new_frames", "test.mp4", frame_count)
    # seg.convertImage("new_frames", "results", "frame100")
    # seg.overlay("results", "results2", "Bliss", "frame100")
    # for i in range(1, 128):
    #     seg.convertImage("test_frames", "test_o_frames", "frame" + str(i))
    #     seg.overlay("test_o_frames", "test_fin_frames", "Bliss", "frame" + str(i))

    # video_funcs.make_video("test_video", "test_fin_frames", "test.mp4", 128)


