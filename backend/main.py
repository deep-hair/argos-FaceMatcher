import time
from Chair import Chair
import os
from objectDetection import Detector
import glob

chair = Chair([0,1200,0,1200],1)
detector = Detector('')

import cv2
cap = cv2.VideoCapture('output_1.mp4')
#cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
t1 = 0
# The device number might be 0 or 1 depending on the device and the webcam
while True:
    t0 = time.time()
    
    ret, frame = cap.read()
    #print(frame.shape)
    if ret : 
        cv2.imshow('frame', frame)
    else : break
    if t0-t1>2: 
        t1 = time.time()
        #print(f' affichage {t1-t0}')
        
        chair.update(frame, detector)
        print('updated')

        #print(time.time()-t1)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()

cv2.destroyAllWindows()
