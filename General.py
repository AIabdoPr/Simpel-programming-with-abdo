"""
The general function to my project is:
Find faces with a computer camera and compare with saved faces and distinguish them from the rest of the faces, while the table helps to assign a name to the faces
"""

# import the libraries we need
import cv2, numpy as np, os
from time import strftime
from training import getImagesAndLabels
from random import *

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

# xml file for get information to track face
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

open("show.s", "w").write("0\n40")
show = 0

# computer camera
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

# yml file in which the faces were saved
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

# Opencv font
font = cv2.FONT_HERSHEY_SIMPLEX

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

path = "dataset/"
i = 0
# run helper table
os.system('start python "tabel.py"')
while 1:
    data = open("show.s", "r").read().split("\n")[0]
    if not  data == str(show):
        show = data
        if show == "0":show = 0
        cam = cv2.VideoCapture(show)

    # get image from camera
    _, img = cam.read()
    # resize image to (640, 480)
    img = cv2.resize(img, (640, 480), interpolation = cv2.INTER_AREA)
    # save image width and height in w_h file
    # open("w_h", "w").write("{0}x{1}".format(img.shape[0], img.shape[1]))

    # convert image colors to gray color
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # find faces from image
    faces = face_detector.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    # send images path from dataset folder in list
    imagesPath = [os.path.join(path,f) for f in os.listdir(path)]
    num = len(imagesPath)# images number

    # face id to last image
    if not(num == 0):# if images number is not 0
        if(i == 0):# Make sure get the number is not repeated
            face_id = str(int(imagesPath[-1].split(".")[1])+1)# last image number + 1
    elif(num == 0 & i == 0):# if images number is 0 and make sure get the number is not repeated
        face_id = 0

    # get names and face id from "Characters_Names.cn" file
    names = []
    if os.path.exists(r"trainer\Characters_Names.cn"):
        cns = open(r"trainer\Characters_Names.cn", "r").read().split('\n')
        del(cns[-1])
        for cn in cns:# send the names on "names" value
            names.append(cn.split('===')[2])

    for (x,y,w,h) in faces:# get face locution and send to (x, y, w, h) values
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)# Draw rectangle around face

        # Obtain ipsilateral id face and likeness ratio
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # While the likeness is greater than 40, the name is placed
        try:
            ratio = int(open("show.s", "r").read().split("\n")[1])
        except:
            ratio = 40
        if (100-confidence >= ratio):
            try:
                id = names[id]
            except:
                id = "Face<{}>".format(id)
            pors = int(100-confidence)
            confidence = "  {0}%".format(pors)
        else:# Press "A" to add a new face
            id = "New Face"
            pors = 0
            confidence = ""
            cv2.putText(img, 'Press "A" to add this new face', (10,30), font, 1, (255,0,255), 2)

            # add a new face while press "A" key
            if(cv2.waitKey(10) & 0xff == ord("a")):
                # save 50 image
                if(i<50):# save while "i<50"
                    if(i == 0):# add a new face info on "Characters_Names.cn"
                        text = "{0}==={1}===Face<{0}>\n".format(face_id, strftime("%d-%m-%Y-%H-%M-%S"))
                        open(r"trainer\Characters_Names.cn", "a+").write(text)
                    
                    i += 1
                    cv2.putText(img, '{}%'.format(i*2), (x+10,h+5), font, 1, (255,255,0), 2)# show the saved image percent
                    # save a image
                    cv2.imwrite("dataset/User." + str(face_id) + '.' + str(i) + ".jpg", gray[y:y+h,x:x+w])
                else:
                    cv2.destroyAllWindows()# destroy a window
                    getImagesAndLabels(cam)# trainer the images
                    i = 0

        # show the information
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,0,255), 2)# show face name
        cv2.putText(img, str(confidence), (pors,25), font, 1, (0,255,255), 1)# show likeness percent
        cv2.line(img, (10,10), (pors+10,10), (0,255,255), 10)# show the likeness ratio as a line
        
    cv2.imshow('image', img)# show the image
    cv2.moveWindow("image", 10,20);# window geometry
    k = cv2.waitKey(10) & 0xff
    if k == 27:# Press 'ESC' for exiting video
        break

cam.release()# close a camera
cv2.destroyAllWindows()# destroy a window