from pytesseract import image_to_string
from PIL import Image
import numpy as np
import cv2
import os


class Translator:
    def __init__(self):
        pass

    def toBinary(self, file):
        img = cv2.imread(os.path.join('./res/',file))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red = np.array([78,32,50])
        upper_red = np.array([132,255,255])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        mask_inv = cv2.bitwise_not(mask)

        res = cv2.bitwise_and(img,img, mask=mask_inv)
        res[res == 0] = 255
        gray = cv2.cvtColor(res,cv2.COLOR_RGBA2GRAY)
        if(file != 'brand.jpg' or file != 'model.jpg'):
            gray = cv2.medianBlur(gray, 7)
        retval, threshold = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY)

        cv2.imwrite('./binary/bin-' + file,threshold)

    def translate(self):
        print('translation...')
        for file in os.listdir("./res"):
            self.toBinary(file);
            txt = image_to_string(Image.open("./binary/bin-" + file))
            if(file != 'brand.jpg' or file != 'model.jpg'):
               txt = ''.join(i for i in txt if i.isdigit())
            print(txt)
