# import the necessary packages
from quantizator.quantizator import Quantizator
from maskerator.maskerator import Maskerator
from cropper.cropper import Cropper
from builder.builder import Builder
import argparse
import imutils
import cv2
import os
import shutil

count = 0

class Compute:
    def __init__(self):
        pass

    def compute(self):
        q = Quantizator()
        m = Maskerator()
        c = Cropper()
        b = Builder()

        # load the image and resize it to a smaller factor so that
        # the shapes can be approximated better
        image = cv2.imread('./temp/image.jpg')
        # resize image
        resized = cv2.resize(image, (960,1280), interpolation=cv2.INTER_AREA)
        cv2.imwrite('./temp/original.jpg',resized)

        q.quantize(32)
        m.mask()
        assemblyInstructions = c.crop()
        b.build(assemblyInstructions)

        with open('./json/data.json', 'r') as f:
            return f.read()
