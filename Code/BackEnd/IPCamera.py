import numpy as np
from cv2 import cv2
import urllib.request as urllib
from datetime import datetime
import threading
import pandas as pd
import os
from enum import Enum
import time

class CameraStatus(Enum):
    Paused = 0
    Started = 1

class PersonBucket:
    def __init__(self):
        self.ageList = [[0, 6], [6, 12], [12, 18], [18, 26], [26, 36], [36, 48], [48, 60], [60, 100]]
        self.ageBucket = [0, 0, 0, 0, 0, 0, 0, 0]
        self.genderList = ['Female', 'Male']
        self.genderBucket = [0, 0]

    def clearAgeBucket(self):
        self.ageBucket = [0, 0, 0, 0, 0, 0, 0, 0]

    def clearGenderBucket(self):
        self.genderBucket = [0, 0]

    def increaseAgeBucket(self, idx):
        self.ageBucket[idx] += 1

    def increaseGenderBucket(self, idx):
        self.genderBucket[idx] += 1

    def findIntervalIdx(self, num):
        i = 0
        for i in range(len(self.ageList)):
            if self.ageList[i][0] <= num < self.ageList[i][-1]:
                return i

class IntervalHandler:
    def __init__(self, lastInterval):
        self.intervals = [[0, 2], [2, 4], [4, 6], [6, 8], [8, 10], [10, 12], [12, 14], [14, 16], [16, 18], [18, 20], [20, 22], [22, 24]]
        self.lastInterval = lastInterval

        self.defaultDate = "1970-01-01 00:00:00"
        if (lastInterval == 0):
            self.lastInterval = self.defaultDate

    def getIntervalID(self, hour):
        for i in range(len(self.intervals)):
            if self.intervals[i][0] <= hour < self.intervals[i][-1]:
                return i

    def getIntervalDateNow(self):
        hour = self.intervals[self.getIntervalID(datetime.now().hour)][0]
        return datetime(datetime.today().year, datetime.today().month, datetime.today().day, hour)

    def isDataSaveable(self):
        dateNow = self.getIntervalDateNow()
        if (self.lastInterval == self.defaultDate):
            self.lastInterval = str(dateNow)
        if (str(self.lastInterval) != str(dateNow)):
            return True
        return False

    def refreshIntervalHour(self):
        self.lastInterval = self.getIntervalDateNow()

class IPCamera:
    def __init__(self, url, name, status, imgType):
        self.url = url
        self.filename = self.getFileNameFromUrl()
        self.path = 'DB/cameras/' + self.filename + '.csv'
        self.imgType = imgType
        self.personBucket = PersonBucket()
        self.intervalHandler = IntervalHandler(self.loadLastSaved())
        self.stopped = False
        self.name = name
        self.status = status
        self.cameraThread = threading.Thread(target=self.ipcamFaceDetect, args=())
        self.writeThread = threading.Thread(target=self.writeCSV, args=())
        self.frame = 0
        self.age_model = cv2.dnn.readNetFromCaffe("BackEnd/Models/age.prototxt", "BackEnd/Models/age.caffemodel")
        self.gender_model = cv2.dnn.readNetFromCaffe("BackEnd/Models/gender.prototxt",
                                                     "BackEnd/Models/gender.caffemodel")
        self.haar_detector = cv2.CascadeClassifier("BackEnd/Models/haarcascade_frontalface_default.xml")

        if (status == CameraStatus.Started):
            self.status = CameraStatus.Paused
            self.startCameraThread()

        self.createCSV()

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

    def loadLastSaved(self):
        if (os.path.isfile(self.path)):
            print(self.path)
            df = pd.read_csv(self.path)
            return df["time"].tail(1).tolist()[0]
        else:
            return 0

    def reloadIntervalData(self):
        if (os.path.isfile(self.path)):
            df = pd.read_csv(self.path)

            lastAgeBucket = df["age"].tail(1).tolist()[0]
            lastAgeBucket = lastAgeBucket.replace('[', '')
            lastAgeBucket = lastAgeBucket.replace(']', '')
            lastAgeBucket = lastAgeBucket.split(', ')
            for i in range(0, len(lastAgeBucket)):
                lastAgeBucket[i] = int(lastAgeBucket[i])

            lastGenderBucket = df["gender"].tail(1).tolist()[0]
            lastGenderBucket = lastGenderBucket.replace('[', '')
            lastGenderBucket = lastGenderBucket.replace(']', '')
            lastGenderBucket = lastGenderBucket.split(',')
            for i in range(0, len(lastGenderBucket)):
                lastGenderBucket[i] = int(lastGenderBucket[i])

            self.personBucket.ageBucket = lastAgeBucket
            self.personBucket.genderBucket = lastGenderBucket

            df.drop(df.tail(1).index, axis=0, inplace=True)
            df.to_csv(self.path, index=False)

    def getFileNameFromUrl(self):
        newUrl = self.url.replace(".", "-")
        newUrl = newUrl.replace(":", "-")
        return newUrl

    def createCSV(self):
        if (os.path.isfile(self.path)):
            return

        interval = pd.DataFrame(
            [[self.intervalHandler.getIntervalDateNow(), self.personBucket.ageBucket, self.personBucket.genderBucket]],
            columns=['time', 'age', 'gender'])
        interval.to_csv(self.path, mode='a', index=False, header=True)

    def writeCSV(self):
        notExist = True
        if (os.path.isfile(self.path)):
            notExist = False

        interval = pd.DataFrame(
            [[self.intervalHandler.getIntervalDateNow(), self.personBucket.ageBucket, self.personBucket.genderBucket]],
            columns=['time', 'age', 'gender'])
        self.personBucket.clearAgeBucket()
        self.personBucket.clearGenderBucket()
        self.intervalHandler.refreshIntervalHour()

        interval.to_csv(self.path, mode='a', index=False, header=notExist)

    def startCameraThread(self):
        if(not self.cameraAlive()):
            return False
        if (self.status == CameraStatus.Paused and not self.cameraThread.isAlive()):
            if (self.intervalHandler.lastInterval == str(self.intervalHandler.getIntervalDateNow())):
                self.reloadIntervalData()

            self.intervalHandler.refreshIntervalHour()
            
            self.status = CameraStatus.Started
            self.stopped = False
            
            self.cameraThread = threading.Thread(target=self.ipcamFaceDetect, args=())
            self.cameraThread.start()

            return True
        return False

    def pauseCameraThread(self):
        if(not self.cameraAlive()):
            self.status = CameraStatus.Paused
            self.stopped = True
            return False
        if (self.status == CameraStatus.Started):
            self.status = CameraStatus.Paused
            self.stopped = True
            return True
        return False

    def cameraAlive(self):
        urlshot = "http://" + self.url + "/" + self.imgType
        try:
            imgResp = urllib.urlopen(urlshot, timeout=5)
            return True
        except:
            return False

    def ipcamFaceDetect(self):
        urlshot = "http://" + self.url + "/" + self.imgType
        x = threading.Thread(target=self.saveImage, args=())
        x.start()
        while not self.stopped:
            try:
                imgResp = urllib.urlopen(urlshot, timeout=5)
                imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
                frame = cv2.imdecode(imgNp, -1)
            except:
                break
            
            if frame is not None:
                self.frame = frame
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.haar_detector.detectMultiScale(gray, 1.2, 5)

                for face in faces:
                    x, y, w, h = face
                    detected_face = frame[int(y):int(y + h), int(x):int(x + w)].copy()
                    img_blob = cv2.dnn.blobFromImage(detected_face, 1, (224, 224), self.MODEL_MEAN_VALUES, swapRB=False)

                    self.age_model.setInput(img_blob)
                    age_pred = self.age_model.forward()
                    agenum = age_pred[0].argmax()
                    self.personBucket.increaseAgeBucket(self.personBucket.findIntervalIdx(agenum))

                    self.gender_model.setInput(img_blob)
                    gender_pred = self.gender_model.forward()[0]
                    gendernum = np.argmax(gender_pred)
                    self.personBucket.increaseGenderBucket(gendernum)

            if (self.intervalHandler.isDataSaveable() and not self.writeThread.isAlive()):
                self.writeThread.start()

        if (not self.writeThread.isAlive()):
            self.writeThread = threading.Thread(target=self.writeCSV, args=())
            self.writeThread.start()

        self.status = CameraStatus.Paused
        self.stopped = True

    def saveImage(self):
        while not self.stopped:
            if self.frame is not None:
                time.sleep(1)
                cv2.imwrite("DB/cameraPhotos/" + self.filename + ".png", self.frame)


'''camera = IPCamera("192.168.0.114:8080", "NagyViktor", CameraStatus.Paused, "shot.jpg")
camera.startCameraThread()'''