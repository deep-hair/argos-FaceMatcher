import os
from typing import Any
import cv2
from deepface import DeepFace
import numpy as np

def format_yolo(source):

    # put the image in square big enough
    col, row, _ = source.shape
    _max = max(col, row)
    resized = np.zeros((_max, _max, 3), np.uint8)
    resized[0:col, 0:row] = source

    return cv2.dnn.blobFromImage(resized, 1/255.0, (640, 640), swapRB=True)

class Detector:

    def __init__(self, model = '', threshold = 0.8) -> None:
        absolutePath  = f'/Users/g0bel1n/PycharmProjects/deep-next-web-app/models/yolov4{model}.'
        self.MODEL = cv2.dnn.readNet(f'{absolutePath}weights', f'{absolutePath}cfg')
        self.THRESHOLD = threshold


    def evaluate(self, img) -> bool:
        formatted_img = format_yolo(img)

        self.MODEL.setInoput(formatted_img)
        output = self.MODEL.forward()
        try : confidence = output[0][0][5]
        except IndexError : confidence = 0

        return self.THRESHOLD<confidence



if __name__=='__main__':
    print (os.getcwd())
    obj = ObjectDetection()