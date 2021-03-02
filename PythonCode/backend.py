import numpy as np
import cv2, time
import urllib.request as urllib
import face_recognition as fr

def ipcam():
    url='http://192.168.0.176:8080/shot.jpg'

    while True:
        imgResp = urllib.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        cv2.imshow('IP Camera', img)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
def webcam():
    video = cv2.VideoCapture(0)

    while True:
        check, frame = video.read()

        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Web Camera", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()
def webcamFaceDetect():
    video_capture = cv2.VideoCapture(0)

    viktor_image = fr.load_image_file("images/image1.png")
    viktor_face_encoding = fr.face_encodings(viktor_image)[0]
    known_face_encondings = [viktor_face_encoding, palvin_face_encoding]
    known_face_names = ["Viktor"]

    while True: 
        ret, frame = video_capture.read()

        rgb_frame = frame[:, :, ::-1]

        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            matches = fr.compare_faces(known_face_encondings, face_encoding)

            name = "Unknown"

            face_distances = fr.face_distance(known_face_encondings, face_encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Webcam Facerecognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList=[[0, 5], [6, 10], [10, 14], [15, 21], [22, 29], [30, 45], [46, 59], [60, 100]]
genderList = ['Female', 'Male']

def find_interval(num):
    for intervals in ageList:
      if intervals[0] <= num <= intervals[-1]:
         return str(intervals[0]) + "-" + str(intervals[-1])
         
def ipcamFaceDetect():
    age_model = cv2.dnn.readNetFromCaffe("age.prototxt", "dex_chalearn_iccv2015.caffemodel")
    gender_model = cv2.dnn.readNetFromCaffe("gender.prototxt", "gender.caffemodel")
    haar_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    url = 'http://192.168.0.176:8080/shot.jpg'
    #video = cv2.VideoCapture(0)
    #video.open(url)
   
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
                  age = find_interval(age_pred[0].argmax())

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

ipcamFaceDetect()