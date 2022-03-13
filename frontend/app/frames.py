import logging
import time
import pandas as pd

import cv2
from yolov5.detect import run

def gen_frames():
    camera = cv2.VideoCapture('rtsp://admin:SFYZEV@78.113.98.174:554/H.264')
    frame_rate = 10
    prev = 0
    n=0
    counter =0

    while True:
        time_elapsed = time.time() - prev
        success, frame = camera.read()

        if time_elapsed > 1. / frame_rate:
            prev = time.time()
        # read the camera frame
            if not success:
                break
            else:
                try :
                    n_new,im = run(img0=frame, view_img=True)
                except:
                    pass
                ret, buffer = cv2.imencode('.jpg', im)
                img = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
