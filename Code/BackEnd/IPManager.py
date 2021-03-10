import numpy as np
import cv2, time
import urllib.request as urllib
import face_recognition as fr
from datetime import datetime
import threading
import json
import pandas as pd
import os.path
import IPCamera

class IPManager:
    def __init__(self):
        self.cameraList = parseCameras()

    def addCamera(self, ipaddr):

    def deleteCamera(self, ipaddr):

    def startCamera(self, ipaddr):

    def stopCamera(self, ipaddr):
   
    def parseCameras():
        cameraList = []

    def persistCamera(self, ipaddr, name):
        path='DB/cameraList.csv'

        notExist = True
        if(os.path.isfile(path)): 
            notExist=False
        
        self.cameraList.push(new IPCamera(ipaddr, name))
        
        interval = pd.DataFrame([[ipaddr, name]], columns=['ipaddress', 'name'])
        interval.to_csv(path, mode='a', index=False, header=notExist)
