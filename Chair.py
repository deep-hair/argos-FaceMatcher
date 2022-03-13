import os
from time import time
import cv2
from cv2 import mean
from matplotlib import pyplot as plt

import numpy as np
from deepface import DeepFace
import pandas as pd
from datetime import datetime
import os
import glob



from objectDetection import Detector


def getSample(camera: cv2.VideoCapture, n_samples = 5) -> list[np.array]:  # type: ignore
    assert camera.isOpened, 'The camera is not active'
    samples = []
    while len(samples)< n_samples :
        success,frame = camera.read()
        if success : samples.append(np.array(frame))
        cv2.waitKey(1000)
    return samples

def get_group_id(identity: str) -> str:
    splitted_str = identity.split('_')
    return f'{splitted_str[1]}_{splitted_str[3]}'

def thresholdMatches(listOfMatch: list[pd.DataFrame], threshold = 0.9, n_required = 3) -> bool:
    return any(match.at['score',n_required]>threshold for match in listOfMatch)
 

class Chair:
    def __init__(self, AREA: list[int], id: int) -> None:
        self.AREA = AREA
        self.isOccupied = False
        self.timeSinceLastChanged = time() # Have it in seconds
        self.timeSinceLastStoreFace = time()
        self.FACE_STORAGE_FREQUENCY = 0.1
        self.image = np.array
        self.id = id
        self.customerID = 0
        self.sampling = False
        self.samples=[]
        self.checkId= True

        #os.mkdir(f'sample{self.id}')
    
    def __changeState(self):
        self.timeSinceLastChanged = time()
        self.isOccupied =  not self.isOccupied

    def __newCustomer(self): # potentially
        self.customerID+=1  

    def __checkNewCustomer(self) -> bool:
        '''
        Check if the person seated is a new customer.
        Number of iterCheck : NumberOfSample^2
        '''

        #TODO penser à supprimer les images au bout d'1h30

        imgsPathList =  ['/'.join(['storedFace',imgPath])  for imgPath in os.listdir('storedFace') if imgPath.endswith('jpg')]
        samplePathList =  ['/'.join([f'sample{self.id}',imgPath]) for imgPath in os.listdir(f'sample{self.id}') if imgPath.endswith('jpg')]


        for imgPath in imgsPathList :
            for sample in samplePathList:
                print(imgPath, sample)
                output = DeepFace.verify(img1_path= imgPath,img2_path = sample,model_name='Facenet512',prog_bar=False, enforce_detection=False )
                print(output)
                if output['verified']:
                    # if there is match
                    return False
        return True

    def __storeFace(self):
        face = DeepFace.detectFace(self.image, target_size = (224, 224), detector_backend = 'retinaface')
        plt.imsave(fname = f'storedFace/chair_{self.id}_customer_{self.customerID}_{datetime.now().strftime("%H_%M_%S")}.jpg', arr= face)
        self.timeSinceLastStoreFace = time() - self.timeSinceLastStoreFace

    def __getFace(self):
        face = DeepFace.detectFace(self.image, target_size = (224, 224), detector_backend = 'retinaface')
        plt.imsave(fname = f'sample{self.id}/sample_{datetime.now().strftime("%H_%M_%S")}.jpg', arr= face)



    def update(self, img, detector:Detector):
        self.image = img[self.AREA[0]:self.AREA[1],self.AREA[2]:self.AREA[3],:]
        if self.sampling:
            print('sampling')
            self.__getFace()

            self.sampling = len(os.listdir(f'sample{self.id}'))<2 
        else:
             # Must be numpy
            stateChanged = (self.isOccupied != detector.evaluate(img))
            timeToStore = (self.timeSinceLastStoreFace> 1./self.FACE_STORAGE_FREQUENCY)
            print('state changed', stateChanged)
            print('is Occupied', self.isOccupied)
            print('evaluation', detector.evaluate(img))
            print('checkID', self.checkId)
            if not stateChanged and timeToStore and self.isOccupied:
                # If the seat stays occupied
                if len([el for el in os.listdir(f'storedFace') if el.startswith(f'chair_{self.id}_customer_{self.customerID}')])<2  :
                    self.__storeFace()


                elif self.checkId :
                    self.checkId = False
                    if self.__checkNewCustomer() or len([imgPath  for imgPath in os.listdir('storedFace') if imgPath.endswith('jpg')])==0:
                            self.__newCustomer()
                            print("ADDING A NEW CUSTOMER")
                    else : print("Not a new customer")


                        
            elif stateChanged:
                self.__changeState()
                if self.isOccupied :
                    self.sampling = True
                else : 
                    self.checkId = True
                    files = glob.glob(f'sample{self.id}')
                    for f in files:
                        os.remove(f)

            else : pass