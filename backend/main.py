import os
import time
import cv2
from Chair import Chair
from objectDetection import Detector

try : os.chdir('backend')
except : pass

#TODO 
# - Multithread for multiple chairs and constant video flow
# - improve sampling with subclasses Sample() etc
# - Make yolov4-tiny work 
    

def runDeepHair_FaceMatcher(source: str) -> tuple[int, float]:
    chair = Chair([0,1200,0,1200],1)
    #detector = Detector()

    cap = cv2.VideoCapture(source)
    fps = cap.get(cv2.CAP_PROP_FPS) # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps
    #cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    t1 = 0
    # The device number might be 0 or 1 depending on the device and the webcam
    while True:
        t0 = time.time()
        videoTime = int(cap.get(cv2.CAP_PROP_POS_FRAMES))/fps
        ret, frame = cap.read()
        print(videoTime)
        
        #print(frame.shape)
        if ret : 
            cv2.imshow('frame', frame)
        else : break
        if t0-t1>2: 
            t1 = time.time()
            #print(f' affichage {t1-t0}')
            
            chair.update(frame, videoTime)
            #print('updated')

            #print(time.time()-t1)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()



    cv2.destroyAllWindows()
    return chair._Chair__customerID, duration

if __name__ =='__main__':
    source = 'output_1.mp4'
    start  = time.time()
    numberOfCustomer, duration = runDeepHair_FaceMatcher(source = source )
    print(f'There was {numberOfCustomer} customers in the {source}. It took {time.time()-start} seconds and the video was {duration} seconds long ')
