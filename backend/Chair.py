from asyncio.log import logger
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

from objectDetection import Detector


# Obsolete
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
 
def noStoredFace() -> bool:
    """
    Return True if there are no stored face images in the storedFace folder
    :return: A boolean value.
    """
    return not [
        imgPath
        for imgPath in os.listdir('storedFace')
        if imgPath.endswith('.jpg')
    ]

class Chair:
    def __init__(self, AREA: list[int], id: int) -> None:
        self.AREA = AREA
        self.__isOccupied = False
        self.__timeSinceLastChanged = time() # Have it in seconds
        self.__timeSinceLastStoreFace = time()
        self.FACE_STORAGE_FREQUENCY = 1
        self.image = np.array
        self.id = id
        self.__customerID = 0
        self.__sampling = False
        self.__checkId= True
        self.timeLastStore = time()
        self.timeLastSample = time()
        self.__storedFaces =0
        self.__storedFacesPerCustomer = 3

        #os.mkdir(f'sample{self.id}')
    
    def __changeState(self):

        self.__timeSinceLastChanged = time()
        self.__isOccupied =  not self.__isOccupied

    def __newCustomer(self): # potentially
        """
        The __newCustomer function is a private function that is used to create a new customer
        """
        self.__customerID+=1  

    def __checkNewCustomer(self) -> bool:
        """
        Check if there is a new customer by comparing the stored face images with the images in the
        sample folder
        :return: a boolean value. If the customer is new, the function returns True. If the customer is
        not new, the function returns False.
        """

        #TODO penser à supprimer les images au bout d'1h30

        imgsPathList =  ['/'.join(['storedFace',imgPath])  for imgPath in os.listdir('storedFace') if imgPath.endswith('jpg')]
        samplePathList =  ['/'.join([f'sample{self.id}',imgPath]) for imgPath in os.listdir(f'sample{self.id}') if imgPath.endswith('jpg')]


        for imgPath in imgsPathList :
            for sample in samplePathList:
                output = DeepFace.verify(img1_path= imgPath,img2_path = sample,model_name='Facenet512',prog_bar=False, enforce_detection=False )
                if output['verified']:
                    print(imgPath,sample)
                    # if there is match
                    return False
        return True

    def __storeFace(self):
        face = DeepFace.detectFace(self.image, target_size = (224, 224), detector_backend = 'retinaface')
        plt.imsave(fname = f'storedFace/chair_{self.id}_customer_{self.__customerID}_{datetime.now().strftime("%H_%M_%S")}.jpg', arr= face)
        self.timeLastStore = time()
        


    def __getAreaFromImg(self,img: np.array )-> np.array:
        """
        Get the area of the image defined by the AREA tuple
        
        :param img: the image to be cropped
        :type img: np.array
        :return: The image cropped to the area of interest.
        """
        return img[self.AREA[0]:self.AREA[1],self.AREA[2]:self.AREA[3],:]

    def __sample(self):

        print('sampling')
        face = DeepFace.detectFace(self.image, target_size = (224, 224), detector_backend = 'retinaface')
        plt.imsave(fname = f'sample{self.id}/sample_{datetime.now().strftime("%H_%M_%S")}.jpg', arr= face)
        self.timeLastSample = time()
        self.__sampling = len(os.listdir(f'sample{self.id}'))<2

    def __printAttributesValues(self):
        """
        Prints some of the attributes and values of the object
        """
        print(time()-self.timeLastStore)
        print('is Occupied', self.__isOccupied)
        print('checkID', self.__checkId)

    def __getStoreFaceConditions(self,detector:Detector )-> tuple[bool,bool]:
        """
        If the state of the detector has changed, the time has come to store a face, the customer is
        occupied and we have not stored enough faces yet, we store a face
        
        :param detector: Detector
        :type detector: Detector
        :return: The return value is a tuple of two booleans. The first boolean is True if the state of
        the detector has changed since the last call to this method. The second boolean is True if the
        time since the last call to this method is greater than the time between calls to store a face.
        """
        stateChanged = (self.__isOccupied != detector.evaluate(self.image))
        timeToStore = (time() - self.timeLastStore> 1./self.FACE_STORAGE_FREQUENCY)
        hasAlreadyStoredEnoughFaces = self.__storedFaces > self.__storedFacesPerCustomer
        return(not stateChanged and timeToStore and self.__isOccupied and not hasAlreadyStoredEnoughFaces and not self.__checkId, stateChanged)


    #TODO Clean the shit out of the update func 
    def update(self, img, detector:Detector):

        """
        This function is the main function of the Face class. It is called every time a frame is
        captured by the camera
        
        :param img: The image to be processed
        :param detector: Detector
        :type detector: Detector
        """
        self.image = self.__getAreaFromImg(img)
        if self.__sampling and time()-self.timeLastSample > 5:
            try : self.__sample()
            except ValueError : logger.info('Could not sample, try again later')

        else:
            self.__printAttributesValues()

            # The above code is checking if the state of the face has changed, if the time to store
            # has elapsed, and if the chair is occupied.
            StoreFaceConditions, stateChanged = self.__getStoreFaceConditions(detector=detector)
            print(stateChanged)

            if StoreFaceConditions :
                try : 
                    self.__storeFace()
                    self.__storedFaces +=1
                    print('>>>> Stored a face')
                except ValueError :  'Could not store face, will try again later'
                

            elif self.__checkId and self.__isOccupied:
                self.__checkId = False
                # Checking if there is a new customer by comparing the stored face images with the
                # images in the sample folder. If there is no match, it means that the customer is
                # new.
                if self.__checkNewCustomer() or noStoredFace() :
                    self.__newCustomer()
                    print("ADDING A NEW CUSTOMER")
                    self.__storedFaces = 0
                else: print("Not a new customer")

            elif stateChanged:
                self.__changeState()
                if self.__isOccupied :
                    self.__sampling = True
                else : 
                    self.__checkId = True
                    
                    files = os.listdir(f'sample{self.id}')
                    for f in files:
                        print(f)
                        os.remove('/'.join([f'sample{self.id}',f]))