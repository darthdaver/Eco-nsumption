# import the necessary packages
from quantizator.quantizator import Quantizator
from maskerator.maskerator import Maskerator
from cropper.cropper import Cropper
from translator.translator import Translator
import argparse
import imutils
import cv2

count = 0

q = Quantizator()
m = Maskerator()
c = Cropper()
t = Translator()

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="path to the input image")
#args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
#image = cv2.imread(args["image"])
#cv2.imwrite('./temp/original.jpg',image)

q.quantize(16)
m.mask()
c.crop()
t.translate()
