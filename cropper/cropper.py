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
            
            #print((x,y,w,h))
            #print(area)

            if (area > 15000 and area < 75000):
                flag = False
                for c_x,c_y in centers :
                    #print(x-cX,y-cY)
                    if((abs(c_x-cX) < 10) and (abs(c_y - cY) < 10)):
                        flag = True
                        break
                if not(flag):
                    cut = original.copy()
                    #print((x,y,w,h))
                    #cv2.imshow('cut',cut)
                    #cv2.waitKey(0)
                    rects.append(cv2.boundingRect(c))
                    cnts.append(c)
                    centers.append((cX,cY))
                    if(w > 2.5*h) :
                        out = cut[y+100:y+100+h-10,x+10:x+w-10]
                        cv2.imwrite('./res/cropped-name.jpg', out)
                    else :
                        out = cut[y+10:y+h-10,x+10:x+w-10]
                        cv2.imwrite('./res/cropped-' + str(count) + '.jpg', out)
                        count += 1

        cv2.drawContours(image, cnts, -1, (0,255,0), 3)
        cv2.imwrite('./temp/contours.png', image)
        #print(centers)
        #print(rects)



        '''print('cropping...')

        padding_h = 0
        padding_w = 0
        count = 0

        img = cv2.imread('./temp/eroded.jpg')
        out = cv2.imread('./temp/original.jpg')
        original = cv2.imread('./temp/original.jpg')
        # find contours in the thresholded image and initialize the
        # shape detector
        for i in [0,1]:
            print(i)
            if(i == 0):
                img = cv2.cvtColor(img.copy(), cv2.COLOR_RGB2GRAY)
                img = cv2.GaussianBlur(img, (5, 5), 0)
                img = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY)[1]
            im2, cnts, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # loop over the contours
            for c in cnts:
                x,y,w,h = cv2.boundingRect(c)
                area = w * h

                #print(cv2.boundingRect(c))
                #print(area)

                if(y < 50):
                    y += h

                if ((area > 15000 and area < 75000) or (i == 0)):
                    out = original[y+padding_h+20:y+padding_h+h+20,x+padding_w+20:x+padding_w+w+20]
                    if(i == 0):
                        prova = img[y+padding_h+20:y+padding_h+h-20,x+padding_w+20:x+padding_w+w-20]
                        padding_h = y
                        padding_w = x
                    if(i != 0):
                        if(w > 2.5*h):
                            cv2.imwrite('./res/cropped-name.jpg', out)
                        else:
                            cv2.imwrite('./res/cropped-' + str(count) + '.jpg', out)
                            count += 1'''
