import numpy as np
import cv2, time
import urllib.request as urllib
import face_recognition as fr
from datetime import datetime
import threading
import json

class myThread (threading.Thread):
    def __init__(self, threadID, ageBucket, genderBucket, intervalHourNow):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.ageBucket = ageBucket
        self.genderBucket = genderBucket
        self.intervalHourNow = intervalHourNow
    def stop(self):
        self.__stop = True
    def run(self):
        print ("Starting " + str(self.threadID))
        IPCamera.saveInterval(self.ageBucket, self.genderBucket, self.intervalHourNow)
        print ("Exiting " + str(self.threadID))
        myThread.stop(self)

class IPCamera:
    intervals=[[0, 2], [2, 4], [4, 6], [6, 8], [8, 10], [10, 12], [12, 14], [14, 16], [16, 18], [18, 20], [20, 22], [22, 24]]
    intervalSavedToday=[False, False, False, False, False, False, False, False, False, False, False, False]
    ageBucket=[0, 0, 0, 0, 0, 0, 0, 0]

    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    ageList=[[0, 6], [6, 12], [12, 18], [18, 26], [26, 36], [36, 48], [48, 60], [60, 100]]
    genderList = ['Female', 'Male']
    genderBucket = [0, 0]

    intervalHourNow = 0

    def getTime():
        now = datetime.now()

        return now.hour

    def saveInterval(ageBucket, genderBucket, intervalHourNow) :
        time = datetime(datetime.today().year, datetime.today().month, datetime.today().day, intervalHourNow)
        data = {}
        data['interval'] = []
        data['interval'].append({
            'time': time.strftime("%Y%m%d%H"),
            'age': ageBucket,
            'gender': genderBucket
        })
        with open('DB/data.json', 'a') as outfile:
            json.dump(data, outfile)
            outfile.write('\n')


    def str_interval(num):
        for intervals in IPCamera.ageList:
            if intervals[0] <= num <= intervals[-1]:
                return str(intervals[0]) + "-" + str(intervals[-1])

    def find_interval_id(num):
        i = 0
        for i in range(len(IPCamera.ageList)) :
            if IPCamera.ageList[i][0] <= num <= IPCamera.ageList[i][-1]:
                return i

    def ipcamFaceDetect(urladdress):
        age_model = cv2.dnn.readNetFromCaffe("BackEnd/age.prototxt", "BackEnd/age.caffemodel")
        gender_model = cv2.dnn.readNetFromCaffe("BackEnd/gender.prototxt", "BackEnd/gender.caffemodel")
        haar_detector = cv2.CascadeClassifier("BackEnd/haarcascade_frontalface_default.xml")

        now1 = datetime.now()
        url = urladdress + "/shot.jpg"
    
        while True:
            imgResp = urllib.urlopen(url)
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgNp, -1)

            if frame is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = haar_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
                for face in faces:
                    x, y, w, h = face
                    timedelay = time.time()
                    detected_face = frame[int(y):int(y+h), int(x):int(x+w)].copy()
                    img_blob = cv2.dnn.blobFromImage(detected_face, 1, (224, 224), IPCamera.MODEL_MEAN_VALUES, swapRB=False)
                    
                    age_model.setInput(img_blob)
                    age_pred = age_model.forward()
                    agenum = age_pred[0].argmax()
                    age = IPCamera.str_interval(agenum)
                    IPCamera.ageBucket[IPCamera.find_interval_id(agenum)] += 1

                    gender_model.setInput(img_blob)
                    gender_class = gender_model.forward()[0]
                    gendernum = np.argmax(gender_class)
                    gender = IPCamera.genderList[gendernum]
                    IPCamera.genderBucket[IPCamera.find_interval_id(gendernum)] += 1

                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                    cv2.putText(frame, age, (x+int(3*w/4), y - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    cv2.putText(frame, gender, (x+int(w/4), y - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                    #if(IPCamera.getTime() - IPCamera.intervalHourNow >= 2) :
                    #print(str(datetime.strptime(datetime.now(), "%H%M%S") - datetime.strptime(now1, "%H%M%S")))
                    if(datetime.now().second % 10 == 0) :
                        IPCamera.intervalHourNow = IPCamera.getTime() - IPCamera.getTime() % 2
                        thread = myThread(1, IPCamera.ageBucket, IPCamera.genderBucket, IPCamera.intervalHourNow)
                        thread.start()
                        IPCamera.ageBucket=[0, 0, 0, 0, 0, 0, 0, 0]
                        IPCamera.genderBucket = [0, 0]
            
            cv2.imshow("IP Cam Facedetection", frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        
        #video.release()
        cv2.destroyAllWindows()

#IPCamera.ipcamFaceDetect('http://192.168.1.100:8080')
IPCamera.ipcamFaceDetect('http://192.168.0.176:8080')
