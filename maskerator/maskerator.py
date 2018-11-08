import cv2
import numpy as np
from PIL import Image


class Maskerator:
    def __init__(self):
        pass

    def mask(self):
        print('masking...')
        image = cv2.imread('./temp/quantum.jpg')

        # Here we are defining range of bluecolor in HSV
        # This creates a mask of blue coloured
        # objects found in the frame.
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_red = np.array([78,32,50])
        upper_red = np.array([132,255,255])

        # The bitwise and of the frame and mask is done so
        # that only the blue coloured objects are highlighted
        # and stored in res
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(image,image, mask= mask)
        cv2.imwrite("./temp/mask.jpg",mask)

        # Apply an erosion to eliminate noise
        kernel = np.ones((2,2),np.uint8)
        erosion = cv2.erode(mask,kernel,iterations = 1)
        #kernel = np.ones((3,3),np.uint8)
        #dilation = cv2.dilate(erosion,kernel,iterations = 2)
        cv2.imwrite("./temp/eroded.jpg",erosion)

        #cv2.imshow('mask',mask)
        #cv2.imshow('res',res)
        #cv2.imshow('image',erosion)
        #cv2.waitKey(0)
