import numpy as np
import cv2, time
import urllib.request as urllib
import face_recognition as fr
from datetime import datetime
import threading
import json
import pandas as pd
import os
import IPCamera as ic
from enum import Enum

class IPManager:
    def __init__(self):
        self.cameraList = self.parseCameras()
        self.cameraThreadList = []
        self.createThreads()

    def __del__(self):
        for camera in self.cameraList :
            camera.stopCamera()

    def addCamera(self, ipaddr, name, status):
        self.persistCamera(ipaddr, name, status)
        
        ipcamera = IPCamera(ipaddr, name, status)
        self.cameraList.append(ipcamera)


    def deleteCamera(self, ipaddr):
        i = 0
        for i in range(len(self.cameraList)) :
            if(self.cameraList[i].url == ipaddr):
                self.cameraList[i].stopCamera()
                self.cameraThreadList.pop(i)
                self.cameraList.pop(i)
                self.deleteCameraFromDB(i)
                

    def startCamera(self, id):
        self.cameraList[id].status = ic.CameraStatus.Started
        self.cameraThreadList[id].start()

    def pauseCamera(self, id):
        self.cameraList[id].status = ic.CameraStatus.Paused
        self.cameraList[id].stopCamera()

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

    def createThreads(self) :
        i = 0
        for i in range(len(self.cameraList)) :
            self.cameraThreadList.append(threading.Thread(target=self.cameraList[i].ipcamFaceDetect, args=()))
            if(self.cameraList[i].status == ic.CameraStatus.Started) :
               self.cameraThreadList[i].start()

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
time.sleep(15)
print(ipm.cameraList[0].status)
ipm.pauseCamera(0)
print(ipm.cameraList[0].status)

for thread in threading.enumerate(): 
    print(thread.name)

#ipm.persistCamera("198", "a", ic.CameraStatus.Paused)
#ipm.deleteCameraFromDB(1)
#ipm.parseCameras()