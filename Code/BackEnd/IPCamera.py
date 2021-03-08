import numpy as np
import cv2, time
import urllib.request as urllib
import face_recognition as fr
from datetime import datetime
import threading
import json
import pandas as pd
import os.path

class myThread (threading.Thread):
    def __init__(self, threadID, ipcamera):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.ipcamera = ipcamera
    def stop(self):
        self.__stop = True
    def run(self):
        print ("Starting " + str(self.threadID))
        self.ipcamera.writeCSV()
        print ("Exiting " + str(self.threadID))
        myThread.stop(self)

class IPCamera:
    def __init__(self, url, name):
        self.url = url
        self.name = name
        self.intervalHourNow = 0
        self.ageBucket=[0, 0, 0, 0, 0, 0, 0, 0]
        self.genderBucket = [0, 0]
        self.intervalSavedToday=[False, False, False, False, False, False, False, False, False, False, False, False]

    intervals=[[0, 2], [2, 4], [4, 6], [6, 8], [8, 10], [10, 12], [12, 14], [14, 16], [16, 18], [18, 20], [20, 22], [22, 24]]
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList=[[0, 6], [6, 12], [12, 18], [18, 26], [26, 36], [36, 48], [48, 60], [60, 100]]
    genderList = ['Female', 'Male']

    def getTime(self):
        now = datetime.now().hour
        return now.hour

    def writeCSV(self):
        notExist = True
        path='DB/' + self.name + '.csv'
        if(os.path.isfile(path)): 
            notExist=False
        time = datetime(datetime.today().year, datetime.today().month, datetime.today().day, self.intervalHourNow)
        interval = pd.DataFrame([[str(time), self.ageBucket, self.genderBucket]], columns=['time', 'age', 'gender'])
        interval.to_csv(path, mode='a', index=False, header=notExist)

    def str_interval(self, num):
        for intervals in self.ageList:
            if intervals[0] <= num <= intervals[-1]:
                return str(intervals[0]) + "-" + str(intervals[-1])

    def find_interval_id(self, num):
        i = 0
        for i in range(len(self.ageList)) :
            if self.ageList[i][0] <= num <= self.ageList[i][-1]:
                return i

    def ipcamFaceDetect(self):
        age_model = cv2.dnn.readNetFromCaffe("BackEnd/Models/age.prototxt", "BackEnd/Models/age.caffemodel")
        gender_model = cv2.dnn.readNetFromCaffe("BackEnd/Models/gender.prototxt", "BackEnd/Models/gender.caffemodel")
        haar_detector = cv2.CascadeClassifier("BackEnd/Models/haarcascade_frontalface_default.xml")

        now1 = datetime.now()
        urlshot = self.url + "/shot.jpg"
        
        self.writeCSV()

        while True:
            imgResp = urllib.urlopen(urlshot)
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgNp, -1)

            if frame is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = haar_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
                for face in faces:
                    x, y, w, h = face
                    timedelay = time.time()
                    detected_face = frame[int(y):int(y+h), int(x):int(x+w)].copy()
                    img_blob = cv2.dnn.blobFromImage(detected_face, 1, (224, 224), self.MODEL_MEAN_VALUES, swapRB=False)
                    
                    age_model.setInput(img_blob)
                    age_pred = age_model.forward()
                    agenum = age_pred[0].argmax()
                    age = self.str_interval(agenum)
                    self.ageBucket[self.find_interval_id(agenum)] += 1

                    gender_model.setInput(img_blob)
                    gender_class = gender_model.forward()[0]
                    gendernum = np.argmax(gender_class)
                    gender = self.genderList[gendernum]
                    self.genderBucket[self.find_interval_id(gendernum)] += 1

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                    cv2.putText(frame, age, (x+int(3*w/4), y - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    cv2.putText(frame, gender, (x+int(w/4), y - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                    #if(datetime.now().hour - self.intervalHourNow >= 2) :
                    #print(str(datetime.strptime(datetime.now(), "%H%M%S") - datetime.strptime(now1, "%H%M%S")))
                    if(datetime.now().second % 10 == 0) :
                        self.intervalHourNow = datetime.now().hour - datetime.now().hour % 2
                        thread = myThread(1, self)
                        thread.start()
                        self.ageBucket=[0, 0, 0, 0, 0, 0, 0, 0]
                        self.genderBucket = [0, 0]
            
            cv2.imshow("IP Cam Facedetection", frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        
        #video.release()
        cv2.destroyAllWindows()

ipm = IPCamera('http://192.168.1.100:8080', 'ipm')
ipm.ipcamFaceDetect()
#ipm = IPCamera('http://192.168.0.176:8080', 'ipv')
#ipm.ipcamFaceDetect()
