from pytesseract import image_to_string
from PIL import Image
import numpy as np
import json
import cv2
import os
import re

class Builder:
    def __init__(self) :
        pass

    def build(self,instructions) :
        print('build...')
        data = {}

        data['type'] = self.identifyHouseholdAppliance(instructions)

        for file in os.listdir("./res") :
            if (file == 'brand.jpg') :
                data['brand'] = self.translate(file)
            elif (file == 'model.jpg') :
                data['model'] = self.translate(file)
            elif (file == 'consumptions.jpg') :
                data['consumptions'] = self.translate(file)
            elif (file == 'refrigerator.jpg') :
                data['refrigerator'] = self.translate(file)
            elif (file == 'freezer.jpg') :
                data['freezer'] = self.translate(file)
            elif (file == 'centrifuge.jpg') :
                data['centrifuge'] = self.translate(file)
            elif (file == 'water.jpg') :
                data['water'] = self.translate(file)
            elif (file == 'dry.jpg') :
                data['dry'] = self.translate(file)
            elif (file == 'kg.jpg') :
                data['kg'] = self.translate(file)
            elif (file == 'noise.jpg') :
                data['noise'] = self.translate(file)
            elif (file == 'noise-wash.jpg') :
                data['noise-wash'] = self.translate(file)
            elif (file == 'noise-dry.jpg') :
                data['noise-dry'] = self.translate(file)

        with open('./json/data.json', 'w') as outfile:
            json.dump(data, outfile)


    def identifyHouseholdAppliance(self, instructions) :
        print('identification...')
        fields = len(instructions)
        property = min(rect[1] for rect in instructions)
        rect = list(filter(lambda y: y[1] == property, instructions))
        os.rename(rect[0][4], './res/consumptions.jpg')

        instructions = [item for item in instructions if item[4] != rect[0][4]]

        if (fields == 3) :
            for i in range(2) :
                property = min(rect[0] for rect in instructions)
                rect = list(filter(lambda y: y[0] == property, instructions))
                if (i == 0) :
                    os.rename(rect[0][4], './res/refrigerator.jpg')
                elif (i == 1) :
                    os.rename(rect[0][4], './res/noise.jpg')
                instructions = [item for item in instructions if item[4] != rect[0][4]]
            return 'Wine Refrigerator'

        if (fields == 4) :
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

        elif (fields == 5) :
            for i in range(4) :
                property = min(rect[0] for rect in instructions)
                rect = list(filter(lambda y: y[0] == property, instructions))
                if (i == 0) :
                    os.rename(rect[0][4], './res/water.jpg')
                elif (i == 1) :
                    os.rename(rect[0][4], './res/dry.jpg')
                elif (i == 2) :
                    os.rename(rect[0][4], './res/kg.jpg')
                elif (i == 3) :
                    os.rename(rect[0][4], './res/noise.jpg')
                instructions = [item for item in instructions if item[4] != rect[0][4]]
            return 'Dishwasher'
        elif (fields == 6) :
            for i in range(3) :
                property = min(rect[0] for rect in instructions)
                rect = list(filter(lambda y: y[0] == property, instructions))
                if (i == 0) :
                    os.rename(rect[0][4], './res/water.jpg')
                elif (i == 1) :
                    os.rename(rect[0][4], './res/kg.jpg')
                elif (i == 2) :
                    os.rename(rect[0][4], './res/centrifuge.jpg')
                instructions = [item for item in instructions if item[4] != rect[0][4]]
            property = min(rect[1] for rect in instructions)
            rect = list(filter(lambda y: y[1] == property, instructions))
            os.rename(rect[0][4], './res/noise-wash.jpg')
            instructions = [item for item in instructions if item[4] != rect[0][4]]
            rect = instructions
            os.rename(rect[0][4], './res/noise-dry.jpg')
            return 'Washing Machine'
        return "What?!"

    def translate(self, file):
        if (self.toBinary(file)):
            txt = image_to_string(Image.open("./binary/bin-" + file))
            if (file != 'brand.jpg' and file != 'model.jpg') :
                txt = ''.join(i for i in txt if i.isdigit())

            if '\n' in txt :
                while ('\n' in txt) :
                    txt = txt.split('\n',1)[1]

            #txt = re.sub(r'[\W_]+', '', txt)

            return txt

    def toBinary(self, file) :
        img = cv2.imread(os.path.join('./res/',file))

        if not img is None :

            if (file != 'brand.jpg' and file != 'model.jpg') :
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                lower_red = np.array([78,32,50])
                upper_red = np.array([132,255,255])

                mask = cv2.inRange(hsv, lower_red, upper_red)
                mask_inv = cv2.bitwise_not(mask)

                res = cv2.bitwise_and(img,img, mask=mask_inv)
                res[res == 0] = 255
                res = cv2.cvtColor(res,cv2.COLOR_RGBA2GRAY)
                res = cv2.medianBlur(res, 3)
                retval, res = cv2.threshold(res, 80, 255, cv2.THRESH_BINARY)
            else :
                res = cv2.GaussianBlur(img, (3, 3), 0)
                res = cv2.cvtColor(res,cv2.COLOR_RGBA2GRAY)
                retval, res = cv2.threshold(res, 150, 255, cv2.THRESH_BINARY)
                #res = img

            cv2.imwrite('./binary/bin-' + file,res)
            return True
        else:
            print('empty image')
            return False
