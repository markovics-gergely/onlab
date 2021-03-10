import numpy as np
import cv2, time
import urllib.request as urllib
import face_recognition as fr
from datetime import datetime
import threading
import pandas as pd
import os.path
from enum import Enum

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
        for i in range(len(self.ageList)) :
            if self.ageList[i][0] <= num < self.ageList[i][-1]:
                return i 

class IntervalHandler:
    def __init__(self):
        self.intervals=[[0, 2], [2, 4], [4, 6], [6, 8], [8, 10], [10, 12], [12, 14], [14, 16], [16, 18], [18, 20], [20, 22], [22, 24]]
        self.intervalSavedToday=[False, False, False, False, False, False, False, False, False, False, False, False]
        self.intervalHourNow = self.intervals[self.getIntervalID(datetime.now().hour)][0]
        self.dateToday = datetime.today().strftime('%Y-%m-%d')

    def getIntervalID(self, hour):
        for i in range(len(self.intervals)) :
            if self.intervals[i][0] <= hour < self.intervals[i][-1]:
                return i
    
    def isDataSaveable(self):
        intervalID = self.getIntervalID(datetime.now().hour)
        intervalstartnow = self.intervals[intervalID][0]
        if(datetime.today().strftime('%Y-%m-%d') != self.dateToday) :
            return True
        if(not self.intervalSavedToday[intervalID] and intervalstartnow != self.intervalHourNow) :
            return True
        #if(datetime.now().second % 10 == 0):
        #    self.intervalHourNow = datetime.now().hour - datetime.now().hour % 2
        #    return True
        return False

    def refreshIntervalHour(self) :
        oldIntervalID = self.getIntervalID(self.intervalHourNow)
        self.intervalSavedToday[oldIntervalID] = True
        
        newIntervalID = self.getIntervalID(datetime.now().hour)
        self.intervalHourNow = self.intervals[newIntervalID][0]

        if(datetime.today().strftime('%Y-%m-%d') != self.dateToday) :
            self.intervalSavedToday=[False, False, False, False, False, False, False, False, False, False, False, False]
            self.dateToday = datetime.today().strftime('%Y-%m-%d')

class IPCamera:
    def __init__(self, url, name, status):
        self.personBucket = PersonBucket()
        self.intervalHandler = IntervalHandler()
        self.url = url
        self.filename = self.getNameFromUrl()
        self.stopped = False
        self.name = name
        self.status = status

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

    def getNameFromUrl(self):
        newUrl = self.url.replace(".", "-") 
        newUrl = newUrl.replace(":", "-")  
        return newUrl

    def writeCSV(self):
        path='DB/cameras/' + self.filename + '.csv'
        time = datetime(datetime.today().year, datetime.today().month, datetime.today().day, self.intervalHandler.intervalHourNow)

        notExist = True
        if(os.path.isfile(path)): 
            notExist=False
        
        interval = pd.DataFrame([[str(time), self.personBucket.ageBucket, self.personBucket.genderBucket]], columns=['time', 'age', 'gender'])
        self.personBucket.clearAgeBucket()
        self.personBucket.clearGenderBucket()
        self.intervalHandler.refreshIntervalHour()

        interval.to_csv(path, mode='a', index=False, header=notExist)
        
    def stopCamera(self):
        self.stopped = True

    def ipcamFaceDetect(self):
        age_model = cv2.dnn.readNetFromCaffe("BackEnd/Models/age.prototxt", "BackEnd/Models/age.caffemodel")
        gender_model = cv2.dnn.readNetFromCaffe("BackEnd/Models/gender.prototxt", "BackEnd/Models/gender.caffemodel")
        haar_detector = cv2.CascadeClassifier("BackEnd/Models/haarcascade_frontalface_default.xml")

        urlshot = "http://" + self.url + "/shot.jpg"
        print(self.name)
        while True:
            imgResp = urllib.urlopen(urlshot)
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgNp, -1)

            if frame is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = haar_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
                for face in faces:
                    x, y, w, h = face
                    detected_face = frame[int(y):int(y+h), int(x):int(x+w)].copy()
                    img_blob = cv2.dnn.blobFromImage(detected_face, 1, (224, 224), self.MODEL_MEAN_VALUES, swapRB=False)
                    
                    age_model.setInput(img_blob)
                    age_pred = age_model.forward()
                    agenum = age_pred[0].argmax()                 
                    self.personBucket.increaseAgeBucket(self.personBucket.findIntervalIdx(agenum))

                    gender_model.setInput(img_blob)
                    gender_pred = gender_model.forward()[0]
                    gendernum = np.argmax(gender_pred)
                    self.personBucket.increaseGenderBucket(gendernum)


                    if(self.intervalHandler.isDataSaveable()) :
                        thread = threading.Thread(target=self.writeCSV, args=())
                        thread.start()
            

            #cv2.imshow("IP Cam Facedetection", frame)

            #key = cv2.waitKey(1)
            #if key == ord('q'):
            #    break

            if(self.stopped) : 
                break

        print("kiért")       
        cv2.destroyAllWindows()

#ipm = IPCamera('192.168.1.100:8080', 'ipcamera')
#ipm = IPCamera('192.168.0.176:8080', 'ipcamera', CameraStatus.Started)
#ipm.ipcamFaceDetect()
