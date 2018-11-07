# import the necessary packages
import argparse
import imutils
import cv2


class Cropper:
    def __init__(self):
        pass

    def crop(self):
        print('cropping...')

        padding_h = 0
        padding_w = 0
        count = 0

        img = cv2.imread('./temp/eroded.jpg')
        out = cv2.imread('./temp/original.jpg')
        original = cv2.imread('./temp/original.jpg')

        img = cv2.cvtColor(img.copy(), cv2.COLOR_RGB2GRAY)
        #cv2.imshow('img',img)
        #cv2.waitKey(0)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        #cv2.imshow('img',img)
        #cv2.waitKey(0)
        img = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY)[1]
        #cv2.imshow('img',img)
        #cv2.waitKey(0)


        # find contours in the thresholded image and initialize the
        # shape detector
        for i in [0,1]:
            #resized = imutils.resize(image, width=300)
            #ratio = image.shape[0] / float(resized.shape[0])

            # convert the resized image to grayscale, blur it slightly,
            # and threshold it
            cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]

            # loop over the contours
            for c in cnts:
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                #c = c.astype("float")
                #c *= ratio
                #c = c.astype("int")

                #cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                # show the output image
                #cv2.imshow("Image", image)
                #cv2.waitKey(0)
                x,y,w,h = cv2.boundingRect(c)
                area = w * h

                if(y < 50):
                    y += h

                if ((area > 15000 and area < 75000) or (i == 0)):
                    #print(cv2.boundingRect(c))
                    #print(area)
                    out = original[y+padding_h+20:y+padding_h+h+20,x+padding_w+20:x+padding_w+w+20]
                    if(i == 0):
                        img = img[y+padding_h+20:y+padding_h+h-20,x+padding_w+20:x+padding_w+w-20]
                        padding_h = y
                        padding_w = x
                    if(i != 0):
                        if(w > 2.5*h):
                            cv2.imwrite('./res/cropped-name.jpg', out)
                        else:
                            cv2.imwrite('./res/cropped-' + str(count) + '.jpg', out)
                            count += 1
