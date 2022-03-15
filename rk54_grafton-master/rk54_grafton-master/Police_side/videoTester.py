from PyQt4 import QtCore, QtGui
import qdarkstyle
import os
import cv2
import numpy as np
import faceRecognition as fr
import math
import requests
import json
import sqlite3
import CameraWidget as c
import sys
import face_recognition
import sqlite3
#URL for messaging

url = 'https://www.fast2sms.com/dev/bulk'


insert=False
f_name=None
IP="192.168.0.1"


person_detected=0
detected=0

# get request
# def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
#   req_params = {
#   'apikey':apiKey,
#   'secret':secretKey,
#   'usetype':useType,
#   'phone': phoneNo,
#   'message':textMessage,
#   'senderid':senderId
#   }
#   return requests.post(reqUrl, req_params)

def person_counter():
  global person_detected
  connection=sqlite3.connect('data.db')
  cursor=connection.cursor()
  select_query="SELECT max(count) FROM hotspot"
  result=cursor.execute(select_query)
  for row in result:
    person_detected=row[0]
    #print("Query result",row[0])
  person_detected=person_detected+1
  connection.close()
  return person_detected

def exit_application():
    """Exit program event handler"""
    sys.exit(1)
    
def run(camera0):
  global f_name
  global insert

  # Get a reference to webcam #0 (the default one)
  video_capture = cv2.VideoCapture(camera0)

  # Load a sample picture and learn how to recognize it.
  face1_image = face_recognition.load_image_file("C:/python/FACE_RECOGNITION 12_51/easiest_real_time_face_recognition-master/dataset/riddhi.jpeg")
  face1_face_encoding = face_recognition.face_encodings(face1_image)[0]

  # Load a sample picture and learn how to recognize it.
  face2_image = face_recognition.load_image_file("C:/python/FACE_RECOGNITION 12_51/easiest_real_time_face_recognition-master/dataset/nishtha.jpg")
  face2_face_encoding = face_recognition.face_encodings(face2_image)[0]

  # Load a sample picture and learn how to recognize it.
  # messi_image = face_recognition.load_image_file("C:/python/FACE_RECOGNITION 12_51/easiest_real_time_face_recognition-master/dataset/riddhi.png")
  # messi_face_encoding = face_recognition.face_encodings(messi_image)[0]

  # Create arrays of known face encodings and their names
  known_face_encodings = [
      face1_face_encoding,
      face2_face_encoding
      # messi_face_encoding
  ]
  known_face_names = [
      "Riddhi",
      "Nishtha"
  ]

  # Initialize some variables
  face_locations = []
  face_encodings = []
  face_names = []
  process_this_frame = True

  while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        print(name)

        if name in known_face_names:
          print("yes")
          spotted=True
          insert=1
          f_name=name
        else:
          insert=0
        

    # Display the resulting image
    cv2.imshow('Smart Surveillance', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  

  # Release handle to the webcam
  video_capture.release()
  cv2.destroyAllWindows()

  if insert:
    connection=sqlite3.connect('data.db')
    print(connection)
    cursor=connection.cursor()
    query="INSERT INTO hotspot VALUES (?,?)"
    result=cursor.execute(query,(f_name,camera0))
    print(result)
    connection.commit()
    connection.close()

    # response = sendPostRequest(URL, 'J3NAJ4PRRLIT9LYXSH0T7XUDMCHDBCMX', 'TYZ2KOWN24R9V4H3', 'stage', '8160756915', 'RIDDHI', 'Someone named '+predicted_name+' is Detected in your area!!!' )
    # print(response.text)
    message="Someone named {} is detected in at {}".format(f_name,camera0)
    payload = "sender_id=FSTSMS&message={}&language=english&route=p&numbers=7016095156".format(message)

    headers = {
    'authorization': "Gkpe7Y3UWOISLxMdVXHDmjJb6zNuf5aTwrt4ivcRo8B29sAPlnQowaeR0DHdvNWk45xpqOShyGlLcVIj",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
  else:
    insert=False


    # global detected
    
    # #This module captures images via webcam and performs face recognition
    # face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    # face_recognizer.read('C:/python/rk54_grafton/FaceRecognition-master/trainingData.yml')#Load saved training data

    # name = {0 : "Nishtha"}


    # cap=cv2.VideoCapture(0)

    # while True:
    #     ret,test_img=cap.read()# captures frame and returns boolean value and captured image
    #     faces_detected,gray_img=fr.faceDetection(test_img)

    #     for (x,y,w,h) in faces_detected:
    #       cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=7)

    #     resized_img = cv2.resize(test_img, (1000, 700))
    #     cv2.imshow('Smart Surveillance ',resized_img)
    #     cv2.waitKey(10)

    #     for face in faces_detected:
    #         (x,y,w,h)=face
    #         roi_gray=gray_img[y:y+w, x:x+h]
    #         label,confidence=face_recognizer.predict(roi_gray)#predicting the label of given image
    #         print("confidence:",confidence)
    #         print("label:",label)
    #         fr.draw_rect(test_img,face)
    #         predicted_name=name[label]
    #         if confidence < 37:#If confidence less than 70 then don't print predicted face text on screen
    #            fr.put_text(test_img,predicted_name,x,y)
    #            detected=1
    #            f=1
    #         else:
    #           detected=0
    #         # print("detected",detected)
    #         center_coordinates=(340,0)
    #         radius=20
    #         color=(0,0,255)
    #         thickness=-1
    #         dot=cv2.circle(test_img,center_coordinates,radius,color,thickness)
    #         cv2.imshow('Smart Surveillance',dot)
    #         gun_x,gun_y=340,0
    #         x1,y1=x+w,y+h
    #         center_coordinates=(int((x+x1)/2),int((y+y1)/2))
    #         print(x,y,w,h)
    #         dot=cv2.circle(test_img,center_coordinates,radius,color,thickness)

    #         # angle between face and center of camera
    #         print(math.degrees(math.atan2(x+w/2-gun_x,y+h/2-gun_y)))
    #         #fixing the coordinates of gun

    #     resized_img = cv2.resize(test_img, (1000, 700))
    #     cv2.imshow('Smart Surveillance ',resized_img)
    #     if cv2.waitKey(10) == ord('q'):#wait until 'q' key is pressed
    #         break
    # if detected:
    #   count=person_counter()
    #   print("count",count)
    #   connection=sqlite3.connect('data.db')
    #   cursor=connection.cursor()
    #   insert_query="INSERT INTO hotspot VALUES (?,?)"
    #   cursor.execute(insert_query,(predicted_name,person_counter()))
    #   connection.commit()
    #   connection.close()
    # cap.release()
    # cv2.destroyAllWindows


    # #get response Code for text message
    # if f==1:
    #   # response = sendPostRequest(URL, 'J3NAJ4PRRLIT9LYXSH0T7XUDMCHDBCMX', 'TYZ2KOWN24R9V4H3', 'stage', '8160756915', 'RIDDHI', 'Someone named '+predicted_name+' is Detected in your area!!!' )
    #   # print(response.text)
    #   message="Someone named {} is detected in your area".format(predicted_name)
    #   payload = "sender_id=FSTSMS&message={}&language=english&route=p&numbers=8160756915".format(message)

    #   headers = {
    #   'authorization': "Gkpe7Y3UWOISLxMdVXHDmjJb6zNuf5aTwrt4ivcRo8B29sAPlnQowaeR0DHdvNWk45xpqOShyGlLcVIj",
    #   'Content-Type': "application/x-www-form-urlencoded",
    #   'Cache-Control': "no-cache",
    #   }
    #   #response = requests.request("POST", url, data=payload, headers=headers)
    #   print(response.text)

def multiple_cam():
  global IP
  app = QtGui.QApplication([])
  app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt())
  app.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
  mw = QtGui.QMainWindow()
  mw.setWindowTitle('Camera GUI')
  mw.setWindowFlags(QtCore.Qt.FramelessWindowHint)

  cw = QtGui.QWidget()
  ml = QtGui.QGridLayout()
  cw.setLayout(ml)
  mw.setCentralWidget(cw)
  mw.showMaximized()

  # Dynamically determine screen width/height
  screen_width = QtGui.QApplication.desktop().screenGeometry().width()
  screen_height = QtGui.QApplication.desktop().screenGeometry().height()

  # Create Camera Widgets 
  username = ''
  password = ''

  # Stream links
  camera0 = 'http://192.168.43.81:8080/video'
  # #camera1 = 'http://192.168.137.95:8080/video'
  # camera2 = 'http://192.168.137.78:8080/video'
  # #camera3 = 'http://192.168.137.98:8080/video'
  # #camera4 = 'http://192.168.137.143:8080/video'
  # #camera5 = 'http://192.168.43.1:8080/video'
  # #camera6 = 'http://192.168.43.1:8080/video'
  # #camera7 = 'http://192.168.43.1:8080/video'

  run(camera0)
  
  # Create camera widgets
  print('Creating Camera Widgets...')
  zero = c.CameraWidget(screen_width//2, screen_height//2, camera0)
  # #one = c.CameraWidget(screen_width//3, screen_height//3, camera1)
  # two = c.CameraWidget(screen_width//3, screen_height//3, camera2)
  # #three = c.CameraWidget(screen_width//3, screen_height//3, camera3)
  # #four = c.CameraWidget(screen_width//3, screen_height//3, camera4)
  # # five = c.CameraWidget(screen_width//3, screen_height//3, camera5)
  # # six = c.CameraWidget(screen_width//3, screen_height//3, camera6)
  # # seven = c.CameraWidget(screen_width//3, screen_height//3, camera7)
  IP=zero.camera_stream_link

  # Add widgets to layout
  print('Adding widgets to layout...')
  ml.addWidget(zero.get_video_frame(),0,0,1,1)
  # #ml.addWidget(one.get_video_frame(),0,1,1,1)
  # ml.addWidget(two.get_video_frame(),0,2,1,1)
  # #ml.addWidget(three.get_video_frame(),1,0,1,1)
  # ml.addWidget(four.get_video_frame(),1,1,1,1)
  # # ml.addWidget(five.get_video_frame(),1,2,1,1)
  # # ml.addWidget(six.get_video_frame(),2,0,1,1)
  # # ml.addWidget(seven.get_video_frame(),2,1,1,1)

  print('Verifying camera credentials...')

  mw.show()

  QtGui.QShortcut(QtGui.QKeySequence('Ctrl+Q'), mw, exit_application)

  if(sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
      QtGui.QApplication.instance().exec_()
  
#multiple_cam()
