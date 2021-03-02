import numpy as np
import cv2, time
import urllib.request as urllib
import face_recognition as fr

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList=[[0, 2], [4, 6], [8, 12], [15, 20], [25, 32], [38, 43], [48, 53], [60, 100]]
genderList = ['Female', 'Male']

def find_interval(num):
    for intervals in ageList:
      if intervals[0] <= num <= intervals[-1]:
         return (intervals[0] + str(" - ") + intervals[-1])
         
def ipcamFaceDetect(urladdress):
    age_model = cv2.dnn.readNetFromCaffe("age.prototxt", "dex_chalearn_iccv2015.caffemodel")
    gender_model = cv2.dnn.readNetFromCaffe("gender.prototxt", "gender.caffemodel")
    haar_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    url = urladdress
   
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
                  img_blob = cv2.dnn.blobFromImage(detected_face, 1, (224, 224), MODEL_MEAN_VALUES, swapRB=False)
                  
                  age_model.setInput(img_blob)
                  age_pred = age_model.forward()
                  age = str(find_interval(age_pred[0].argmax()))

                  gender_model.setInput(img_blob)
                  gender_class = gender_model.forward()[0]
                  gender = genderList[np.argmax(gender_class)]

                  cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                  cv2.putText(frame, age, (x+int(3*w/4), y - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                  cv2.putText(frame, gender, (x+int(w/4), y - 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        
        cv2.imshow("IP Cam Facedetection", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    
    #video.release()
    cv2.destroyAllWindows()

ipcamFaceDetect('http://192.168.1.100:8080/shot.jpg')