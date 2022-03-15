import os
import cv2
import numpy as np
import faceRecognition as fr
import math
import requests
import json

#URL for messaging
URL = 'https://www.sms4india.com/api/v1/sendCampaign'

# get request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  return requests.post(reqUrl, req_params)

#This module captures images via webcam and performs face recognition
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('C:/python/FaceRecognition-master/trainingData.yml')#Load saved training data

name = {0 : "Priyanka",1 : "Kangana"}


cap=cv2.VideoCapture(0)

while True:
    ret,test_img=cap.read()# captures frame and returns boolean value and captured image
    faces_detected,gray_img=fr.faceDetection(test_img)



    for (x,y,w,h) in faces_detected:
      cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=7)

    resized_img = cv2.resize(test_img, (1000, 700))
    cv2.imshow('face detection Tutorial ',resized_img)
    cv2.waitKey(10)


    for face in faces_detected:
        (x,y,w,h)=face
        roi_gray=gray_img[y:y+w, x:x+h]
        label,confidence=face_recognizer.predict(roi_gray)#predicting the label of given image
        print("confidence:",confidence)
        print("label:",label)
        fr.draw_rect(test_img,face)
        predicted_name=name[label]
        if confidence < 37:#If confidence less than 37 then don't print predicted face text on screen
           fr.put_text(test_img,predicted_name,x,y)
           f=1
        center_coordinates=(340,0)
        radius=20
        color=(0,0,255)
        thickness=-1
        dot=cv2.circle(test_img,center_coordinates,radius,color,thickness)
        cv2.imshow('face recognition turorial',dot)
        gun_x,gun_y=340,0
        x1,y1=x+w,y+h
        center_coordinates=(int((x+x1)/2),int((y+y1)/2))
        print(x,y,w,h)
        dot=cv2.circle(test_img,center_coordinates,radius,color,thickness)
        print(math.degrees(math.atan2(x+w/2-gun_x,y+h/2-gun_y)))
        #fixing the coordinates of gun

    resized_img = cv2.resize(test_img, (1000, 700))
    cv2.imshow('face recognition tutorial ',resized_img)
    if cv2.waitKey(10) == ord('q'):#wait until 'q' key is pressed
        break

# get response
#if f==1:
 #   response = sendPostRequest(URL, 'J3NAJ4PRRLIT9LYXSH0T7XUDMCHDBCMX', 'TYZ2KOWN24R9V4H3', 'stage', '7016095156', 'RIDDHI', 'Someone named '+predicted_name+' Detected!!!' )
  #  print(response.text)

cap.release()
cv2.destroyAllWindows

