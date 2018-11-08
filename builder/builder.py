from pytesseract import image_to_string
from PIL import Image
import numpy as np
import json
import cv2
import os

class Builder:
    def __init__(self):
        pass

    def build(self,instructions):
        data = {}

        #data['type'] = identifyHouseholdAppliance(instructions)

        print(self.identifyHouseholdAppliance(instructions))

        #for file in os.listdir("./res"):
        #    if(file == 'brand.jpg')


    def identifyHouseholdAppliance(self, instructions):
        print('identification...')
        fields = len(instructions)
        property = min(rect[1] for rect in instructions)
        rect = list(filter(lambda y: y[1] == property, instructions))
        os.rename(rect[0][4], './res/consumptions.jpg')

        instructions = [item for item in instructions if item[4] != rect[0][4]]

        if (fields == 3):
            for i in range(2) :
                property = min(rect[0] for rect in instructions)
                rect = list(filter(lambda y: y[0] == property, instructions))
                if (i == 0) :
                    os.rename(rect[0][4], './res/refrigerator.jpg')
                elif (i == 1) :
                    os.rename(rect[0][4], './res/noise.jpg')
                instructions = [item for item in instructions if item[4] != rect[0][4]]
            return 'Wine Refrigerator'

        if (fields == 4):
            for i in range(3) :
                property = min(rect[0] for rect in instructions)
                rect = list(filter(lambda y: y[0] == property, instructions))
                if (i == 0) :
                    os.rename(rect[0][4], './res/refrigerator.jpg')
                elif (i == 1) :
                    os.rename(rect[0][4], './res/freezer.jpg')
                elif (i == 2) :
                    os.rename(rect[0][4], './res/noise.jpg')
                instructions = [item for item in instructions if item[4] != rect[0][4]]
            return 'Refrigerator'

        elif(fields == 5) :
            sample = (instructions[0][0],instructions[0][1])
            check = list(filter(lambda y: abs(y[0] - sample[0]) < 10 and abs(y[1] - sample[1]) < 10, instructions))
            if(len(check) == 4) :
                for i in range(3) :
                    property = min(rect[0] for rect in instructions)
                    rect = list(filter(lambda y: y[0] == property, instructions))
                    if (i == 0) :
                        os.rename(rect[0][4], './res/refrigerator.jpg')
                    elif (i == 1) :
                        os.rename(rect[0][4], './res/freezer.jpg')
                    elif (i == 2) :
                        os.rename(rect[0][4], './res/noise.jpg')
                    instructions = [item for item in instructions if item[4] != rect[0][4]]
                return 'Dishwasher'
            else :
                property = max(rect[1] for rect in instructions)
                rect = list(filter(lambda y: y[1] == property, instructions))
                os.rename(rect[0][4], '.res/noise-wash.jpg')
                instructions = [item for item in instructions if item[4] != rect[0][4]]

                for i in range(3) :
                    property = min(rect[0][0] for rect in instructions)
                    rect = list(filter(lambda y: y[0] == property, instructions))
                    if (i == 0) :
                        os.rename(rect[0][4], 'water.jpg')
                    elif (i == 1) :
                        os.rename(rect[0][4], 'kg.jpg')
                    elif (i == 2) :
                        os.rename(rect[0][4], 'centrifuge.jpg')
                    instructions = [item for item in instructions if item[4] != rect[0][4]]

                rect = instructions
                os.rename(rect[0][4], 'noise-dry.jpg')

                return 'Washing Machine'
        return "What?!"
    def translate(self, filesList):
        print('translation...')
        for file in filesList:
            self.toBinary(file);
            txt = image_to_string(Image.open("./binary/bin-" + file))
            if(file != 'brand.jpg' or file != 'model.jpg'):
               txt = ''.join(i for i in txt if i.isdigit())
            print(txt)

    def toBinary(self, type):
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
