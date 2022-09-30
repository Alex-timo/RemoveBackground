import os
import numpy as np
import cv2
from glob import glob
from tqdm import tqdm
import tensorflow as tf
from tensorflow.keras.utils import CustomObjectScope
from metrics import dice_loss, dice_coef, iou
from PIL import Image
from os.path import isfile, join
import matplotlib.pyplot as plt
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"



""" Global parameters """
H = 512
W = 512


""" Creating a directory """


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def show(img):
    plt.imshow(img)
    plt.show()


def overlay(input_path, background_input_path, output_path, background_file_name, foreground_file_name):
    create_dir(output_path)
    # Opening the primary image (used in background)
    img1 = Image.open(background_input_path + "/" + background_file_name)

    # Opening the secondary image (overlay image)
    img2 = Image.open(input_path + "/" + foreground_file_name)

    # Pasting img2 image on top of img1
    # starting at coordinates (0, 0)
    img1.paste(img2, (0, 0), mask=img2)

    img1.save(output_path + "/" + foreground_file_name, "PNG")

    # Displaying the image
    # img1.show()


def convertImage(input_path, output_path, file_name):
    create_dir(output_path)

    img = Image.open(input_path + "/" + file_name)
    img = img.convert("RGBA")

    datas = img.getdata()

    newData = []

    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(output_path + "/" + file_name)
    print("Successful")


def segmentation(input_path, output_path, color):
    """ Seeding """
    np.random.seed(42)
    tf.random.set_seed(42)

    """ Directory for storing files """
    create_dir(output_path)

    """ Loading model: DeepLabV3+ """
    with CustomObjectScope({'iou': iou, 'dice_coef': dice_coef, 'dice_loss': dice_loss}):
        model = tf.keras.models.load_model("model.h5")

    # model.summary()

    """ Load the dataset """
    data_x = glob(input_path + "\*")

    for path in tqdm(data_x, total=len(data_x)):
         """ Extracting name """
         name = path.split("\\")[-1].split(".")[0]
         print("name is: " + name)

         """ Read the image """
         image = cv2.imread(path, cv2.IMREAD_COLOR)
         h, w, _ = image.shape
         x = cv2.resize(image, (W, H))
         x = x/255.0
         x = x.astype(np.float32)
         x = np.expand_dims(x, axis=0)

         """ Prediction """
         # test = model.predict(x)
         # print(test.shape)

         y = model.predict(x)[0]
         y = cv2.resize(y, (w, h))
         y = np.expand_dims(y, axis=-1)
         print(y.shape)
         y = y > 0.5

         photo_mask = y
         background_mask = np.abs(1-y)

         # cv2.imwrite(f"remove_bg2\{name}.png", photo_mask*255)
         # cv2.imwrite(f"remove_bg2\{name}.png", background_mask*255)

         # cv2.imwrite(f"remove_bg2\{name}.png", image * photo_mask)
         # cv2.imwrite(f"remove_bg2\{name}.png", image * background_mask)


         masked_photo = image * photo_mask
         background_mask = np.concatenate([background_mask, background_mask, background_mask], axis=-1)

         if color == 1:
            background_mask = background_mask * [255, 255, 255]
         elif color == 2:
            background_mask = background_mask * [255, 0, 0]
         elif color == 3:
            background_mask = background_mask * [0, 255, 0]
         elif color == 4:
            background_mask = background_mask * [0, 0, 255]
         elif color == 5:
            background_mask = background_mask * [0, 0, 0]
         elif color == 6:
            background_mask = background_mask * [255, 255, 0]
         elif color == 7:
            background_mask = background_mask * [255, 0, 255]
         elif color == 8:
            background_mask = background_mask * [0, 255, 255]
         else:
            background_mask = background_mask * [255, 255, 255]

         final_photo = masked_photo + background_mask
         cv2.imwrite(f"{output_path}\{name}.png", final_photo)



def black_white_segmentation(input_path, output_path):
    """ Seeding """
    np.random.seed(42)
    tf.random.set_seed(42)

    """ Directory for storing files """
    create_dir(output_path)

    """ Loading model: DeepLabV3+ """
    with CustomObjectScope({'iou': iou, 'dice_coef': dice_coef, 'dice_loss': dice_loss}):
        model = tf.keras.models.load_model("model.h5")

    # model.summary()

    """ Load the dataset """
    data_x = glob(input_path + "\*")

    for path in tqdm(data_x, total=len(data_x)):
         """ Extracting name """
         name = path.split("\\")[-1].split(".")[0]
         print("name is: " + name)

         """ Read the image """
         image = cv2.imread(path, cv2.IMREAD_COLOR)
         h, w, _ = image.shape
         x = cv2.resize(image, (W, H))
         x = x/255.0
         x = x.astype(np.float32)
         x = np.expand_dims(x, axis=0)

         """ Prediction """
         # test = model.predict(x)
         # print(test.shape)

         y = model.predict(x)[0]
         y = cv2.resize(y, (w, h))
         y = np.expand_dims(y, axis=-1)
         print(y.shape)
         y = y > 0.5

         photo_mask = np.abs(1 - y)
         background_mask = y


         cv2.imwrite(f"{output_path}\{name}.png", photo_mask*255)
         cv2.imwrite(f"{output_path}\{name}.png", background_mask*255)


def get_contours(input_path, output_path, original_path, file_name):
    create_dir(output_path)
    fp = input_path + "/" + file_name  #"bw1.jpeg"
    img = cv2.imread(fp)

    img_2 = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(img_2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    editedFrame = img_2.copy()
    frameHeight, frameWidth = img_2.shape

    fp = original_path + "/" + file_name
    print(fp)
    img3 = cv2.imread(fp)
    # show(img3)
    # img4 = cv2.cvtColor(img3.copy(), cv2.COLOR_BGR2GRAY)
    # show(img4)
    editedFrame2 = img3.copy()

    font = cv2.FONT_HERSHEY_SIMPLEX
    numpeople = 0
    contoursInZone = []
    print("contours " + str(len(contours)))
    for cntr in contours:
        x, y, w, h = cv2.boundingRect(cntr)
        print(cv2.contourArea(cntr))
        if cv2.contourArea(cntr) >= 4750:  # if the vehicle contour is in the relevant zone and size is big enough
            cv2.drawContours(editedFrame2, cntr, -1, (0, 255, 255), 3)
            contoursInZone.append(cntr)
            numpeople += 1
            # get the xmin, ymin, width, and height coordinates from the contours
            (x, y, w, h) = cv2.boundingRect(cntr)
    # cv2.putText(editedFrame, "people counted: " + str(numpeople), (frameWidth//4, frameHeight//4), font, 1, (255, 255, 255), 5)
    cv2.putText(editedFrame2, "people counted: " + str(numpeople), (50, 50), font, 1, (255, 255, 255), 5)
    cv2.imwrite(output_path + "/" + file_name, editedFrame2)
