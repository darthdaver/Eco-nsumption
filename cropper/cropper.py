# import the necessary packages
import argparse
import imutils
import cv2
import math


class Cropper:
    def __init__(self):
        pass

    def crop(self):
        original = cv2.imread('./temp/original.jpg')
        image = cv2.imread('./temp/eroded.jpg')
        im_bw = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        (thresh, im_bw) = cv2.threshold(im_bw, 60, 255, 0)

        im2, contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        instructions = []
        centers = []
        rects = []
        cnts = []
        count = 0
        for c in contours:
            M = cv2.moments(c)
            cX = math.ceil(M["m10"] / (M["m00"] + 0.1))
            cY = math.ceil(M["m01"] / (M["m00"] + 0.1))

            x,y,w,h = cv2.boundingRect(c)
            area = w * h

            if (area > 10000 and area < 75000):
                flag = False
                for c_x,c_y in centers :
                    if((abs(c_x-cX) < 10) and (abs(c_y - cY) < 10)):
                        flag = True
                        break
                if not(flag):
                    cut = original.copy()
                    rects.append(cv2.boundingRect(c))
                    cnts.append(c)
                    centers.append((cX,cY))
                    if(w > 2.5*h) :
                        out = cut[y+100:y+100+h,x+10:x+w+10]
                        cv2.imwrite('./res/model.jpg', out)
                        out = cut[y+100:y+100+h,math.ceil(x-(w/2+w/4)):math.ceil(x-(w/2)) + 180]
                        cv2.imwrite('./res/brand.jpg', out)
                    elif(y > 150) :
                        out = cut[y+10:y+h,x+10:x+w+10]
                        cv2.imwrite('./res/cropped-' + str(count) + '.jpg', out)
                        instructions.append((x,y,w,h,'./res/cropped-' + str(count) + '.jpg'))
                        count += 1

        cv2.drawContours(image, cnts, -1, (0,255,0), 3)
        cv2.imwrite('./temp/contours.png', image)
        return instructions
