from sklearn.cluster import MiniBatchKMeans
import numpy as np
import argparse
import cv2

class Quantizator:
    def __init__(self):
        pass

    def quantize(self, clusters):
        print('quantization...')

        image = cv2.imread('./temp/original.jpg')

        (h, w) = image.shape[:2]

        # convert the image from the RGB color space to the L*a*b*
        # color space -- since we will be clustering using k-means
        # which is based on the euclidean distance, we'll use the
        # L*a*b* color space where the euclidean distance implies
        # perceptual meaning
        image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        # reshape the image into a feature vector so that k-means
        # can be applied
        image = image.reshape((image.shape[0] * image.shape[1], 3))

        # apply k-means using the specified number of clusters and
        # then create the quantized image based on the predictions
        clt = MiniBatchKMeans(n_clusters = clusters)
        labels = clt.fit_predict(image)
        quantum = clt.cluster_centers_.astype("uint8")[labels]

        # reshape the feature vectors to images
        quantum = quantum.reshape((h, w, 3))

        # convert from L*a*b* to RGB
        quantum = cv2.cvtColor(quantum, cv2.COLOR_LAB2BGR)

        # display the images and wait for a keypress
        #cv2.imshow("image", quantum)
        #cv2.waitKey(0)

        cv2.imwrite('./temp/quantum.jpg',quantum)
