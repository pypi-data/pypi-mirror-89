import cv2
import os
import math
import pydicom
import numpy as np
from imutils import paths
from scipy import ndimage


# Overview:
# This file contains the code for generalised processing of images

# Reading image from path
def read_image(path):
    img = cv2.imread(path)
    return img


# Displaying an image
def show_image(img, title='img'):
    cv2.imshow(title, img)
    cv2.waitKey(0)  # Press any key to quit.


# Writing an image
def write_image(filepath, img):
    cv2.imwrite(filepath, img)


# Inverting (converting to negative)
def inverting(img):
    invert = 255 - img
    return invert


# Making an image grayscale
def gray_scale(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


# Resizing image according to the length and width specified.
def resize(img, length, width):
    img = cv2.resize(img, (length, width))
    return img


# Applying Gaussian blurring according to the kernel specified. (Smoothing of image)
def gaussian_blurring(img, ksize=(21, 21)):
    blur = cv2.GaussianBlur(img, ksize=ksize, sigmaX=0, sigmaY=0)
    return blur


# Extracting features using ORB (Oriented Fast and Rotated Brief)
def orb_features(img):
    orb = cv2.ORB_create()
    kp, des = orb.detectAndCompute(img, None)
    feat = cv2.drawKeypoints(img, kp, None)
    return feat, des


# Returns the array data of images and their labels (entire path)
def get_images(path):
    path = list(paths.list_images(path))
    data = []
    labels = []
    for imagePath in path:
        label = imagePath.split(os.path.sep)[-2]
        image = read_image(imagePath)
        data.append(image)
        labels.append(label)
    data = np.array(data, dtype="float32")
    labels = np.array(labels)

    return data, labels


# .dcm images to .png images
def dcm_to_png(input_directory, output_directory):
    img_list = [f for f in os.listdir(input_directory)]
    total = len(img_list)
    ct = 0
    for i in img_list:
        ct = ct + 1
        print(f'Written image {ct}/{total}')
        if i.endswith('.dcm'):
            ds = pydicom.read_file(input_directory + i)  # reads the image
            img = ds.pixel_array
            try:
                cv2.imwrite(output_directory + i.replace('.dcm', '.png'), img)
            except:
                pass


# Removing noise from background of colored images
def denoise(img):
    return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)


# Converting image to binary
def binarization(img):
    ret, imgf = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY, cv2.THRESH_OTSU)
    return imgf


# To perform erosion on an image
def erode(img):
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(img, kernel, iterations=1)
    return erosion


# Find contours of an image
def find_contours(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


# To sharpen an image
def sharpen(img):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = cv2.filter2D(img, -1, kernel)
    return img


# To find edged image
def edging(img):
    canny = cv2.Canny(img, 75, 200)
    return canny


# Autorotate an image
def autorotate(img):
    orig = img.copy()
    img_gray = gray_scale(img)
    img_edges = cv2.Canny(img_gray, 100, 100, apertureSize=3)
    lines = cv2.HoughLinesP(img_edges, 1, math.pi / 180, 100, minLineLength=100, maxLineGap=5)
    angles = []
    for [[x1, y1, x2, y2]] in lines:
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)
    median_angle = np.median(angles)
    rotated = ndimage.rotate(orig, median_angle)
    return rotated
