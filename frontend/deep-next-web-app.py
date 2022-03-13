import threading
import time

import cv2

from app import app
from yolov5.detect import run


def gen_frames():
    camera = cv2.VideoCapture('rtsp://admin:SFYZEV@78.113.98.174:554/H.264')
    frame_rate = 10
    prev = 0
    try :
        with open('app/static/counter.txt') as f:
            for line in f:
                last_line = line
        n=int(last_line.split(',')[1])
    except:
        n=0
    counter = n
    while True:
        time_elapsed = time.time() - prev
        success, frame = camera.read()
        if time_elapsed > 1. / frame_rate:
            prev = time.time()
            if not success:
                break
            try:
                n_new,im = run(img0=frame, view_img=True)
                if n_new>n:
                    counter+=1
                with open('app/static/counter.txt', 'a') as file:
                    file.writelines("{0},{1}\n".format(time.strftime("%d:%m:%Y:%H:%M:%S", time.localtime()), counter))
                n= n_new
            except:
                n=0

if __name__ == '__main__':
    threads = [threading.Thread(target=gen_frames), threading.Thread(target=app.run(host='0.0.0.0', port=5000))]
    for thread in threads :
        thread.start()
    for thread in threads :
        thread.join()
