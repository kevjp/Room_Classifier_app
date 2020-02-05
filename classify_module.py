# USAGE
# python classify.py --model fashion.model --labelbin mlb.pickle --image examples/example_01.jpg

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras import backend as K
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


class Classify_image:

    def __init__(self, model, labelbin):
        self.model = model
        self.labelbin = labelbin
        # load the trained convolutional neural network and the multi-label binarizer
        print("[INFO] loading network...")
        print("extra check")
        self.loaded_model = load_model(self.model)
        self.mlb = pickle.loads(open(self.labelbin, "rb").read())

        print(self.model)


    def load_image(self, image_path):
        # load the image
        image = cv2.imread(image_path)
        self.output = imutils.resize(image, width=400)

        # pre-process the image for classification
        image = cv2.resize(image, (224, 224))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        self.image = np.expand_dims(image, axis=0)

    def classify_image(self):

        # classify the input image then find the indexes of the two class
        # labels with the *largest* probability
        print("[INFO] classifying image...")
        proba = self.loaded_model.predict(self.image)[0]
        # K.clear_session()
        idxs = np.argsort(proba)[::-1][:2]
        idxs = np.argsort(proba)[::-1]

        # loop over the indexes of the high confidence class labels
        labels = []
        for (i, j) in enumerate(idxs):
            if proba[j] >= 0.5:
                # build the label and draw the label on the image
                label = "{}: {:.2f}%".format(self.mlb.classes_[j], proba[j] * 100)
                labels.append(label)
                cv2.putText(self.output, label, (10, (i * 30) + 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        return labels

        # show the probabilities for each of the individual labels
        for (label, p) in zip(self.mlb.classes_, proba):
        	print("{}: {:.2f}%".format(label, p * 100))

        # show the output image
        # cv2.imshow("Output", self.output)
        # cv2.waitKey(0)


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", required=True,
        help="path to trained model model")
    ap.add_argument("-l", "--labelbin", required=True,
        help="path to label binarizer")
    ap.add_argument("-i", "--image", required=True,
        help="path to input image")
    args = vars(ap.parse_args())


    # classify = Classify_image(args["model"], args["labelbin"], args["image"])
    # classify.load_image()
    # classify.classify_image()



if __name__ == "__main__":
    main()
