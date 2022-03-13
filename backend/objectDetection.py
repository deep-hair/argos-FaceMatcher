import os
from typing import Any
import cv2
from deepface import DeepFace
from matplotlib import pyplot as plt
import numpy as np

def format_yolo(source):

    # put the image in square big enough
    col, row, _ = source.shape
    _max = max(col, row)
    resized = np.zeros((_max, _max, 3), np.uint8)
    resized[0:col, 0:row] = source

    return cv2.dnn.blobFromImage(resized, 1/255.0, (640, 640), swapRB=True)

class Detector:

    def __init__(self, model = '', threshold = 0.4) -> None:
        absolutePath  = f'/Users/g0bel1n/PycharmProjects/deep-next-web-app/models/yolov4{model}.'
        self.MODEL = cv2.dnn.readNet(f'{absolutePath}weights', f'{absolutePath}cfg')
        self.THRESHOLD = threshold
        self.CLASSES = []
        with open("models/coco-names.txt", "r") as f:
            self.CLASSES = [line.strip() for line in f.readlines()]


    def evaluate(self, img) -> bool:

        formatted_img = format_yolo(img)
        plt.imshow(img)
        self.MODEL.setInput(formatted_img)
        output = self.MODEL.forward()
        #output = output[output[:,5]>self.THRESHOLD]

        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            #print(self.CLASSES[class_id], confidence)
            if class_id == 0 and confidence > self.THRESHOLD : 
                return True
        return False


if __name__=='__main__':
    print (os.getcwd())
    obj = Detector()