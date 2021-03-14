import numpy as np
from cv2 import cv2
import time
import urllib.request as urllib
from datetime import datetime
import threading
import pandas as pd
import os.path
import IPCamera as ic
from enum import Enum

class IPManager:
    def __init__(self):
        self.cameraList = self.parseCameras()

    def addCamera(self, ipaddr, name, status):
        self.persistCamera(ipaddr, name, status)
        
        ipcamera = ic.IPCamera(ipaddr, name, status)
        self.cameraList.append(ipcamera)

    def deleteCamera(self, id):
        self.pauseCamera(id)
        self.cameraList.pop(id)
        self.deleteCameraFromDB(id)        

    def startCamera(self, id):
        self.cameraList[id].startCameraThread()

    def pauseCamera(self, id):
        self.cameraList[id].pauseCameraThread()

    def parseCameras(self):
        clist = []
        path='DB/cameraList.csv'
        df = pd.read_csv(path)

        iplist = df["ipaddress"].tolist()
        namelist = df["name"].tolist()
        statuslist = df["status"].tolist()

        i = 0
        for i in range(len(iplist)) :
            ipcamera = ic.IPCamera(iplist[i], namelist[i], ic.CameraStatus(statuslist[i]))
            clist.append(ipcamera)

        return clist

    def persistCamera(self, ipaddr, name, status):
        path='DB/cameraList.csv'

        notExist = True
        if(os.path.isfile(path)): 
            notExist=False
        
        df = pd.read_csv(path, usecols= ['ipaddress'])
        for b in df["ipaddress"].isin([ipaddr]).tolist() :
            if(b) :
                return False
        
        writer = pd.DataFrame([[ipaddr, name, status]], columns=['ipaddress', 'name', 'status'])
        writer.to_csv(path, mode='a', index=False, header=notExist)

        return True

    def deleteCameraFromDB(self, id) :
        path='DB/cameraList.csv'

        if(not os.path.isfile(path)): 
            return

        df = pd.read_csv(path)
        df.drop(id, axis=0, inplace=True)
        df.to_csv(path, index=False)

        url = self.cameraList[id].getNameFromUrl()

        path = "DB/cameras/" + url + ".csv"
        if(os.path.isfile(path)): 
            os.remove(path)


ipm = IPManager()

ipm.startCamera(0)
print(ipm.cameraList[0].status)

time.sleep(10)

ipm.pauseCamera(0)
print(ipm.cameraList[0].status)

os._exit(0)

