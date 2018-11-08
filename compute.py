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

q = Quantizator()
m = Maskerator()
c = Cropper()
b = Builder()

if (os.path.exists('./temp')) :
    shutil.rmtree('./temp')
    os.mkdir('./temp')
else :
	os.mkdir('./temp')
if (os.path.exists('./res')) :
    shutil.rmtree('./res')
    os.mkdir('./res')
else :
	os.mkdir('./res')
if (os.path.exists('./binary')) :
    shutil.rmtree('./binary')
    os.mkdir('./binary')
else :
	os.mkdir('./binary')

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
cv2.imwrite('./temp/original.jpg',image)

q.quantize(32)
m.mask()
assemblyInstructions = c.crop()
b.build(assemblyInstructions)
#print(assemblyInstructions)
#t.translate(assemblyInstructions)
