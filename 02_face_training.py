''''
Training Multiple Faces stored on a DataBase:
	==> Each face should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model will be saved on trainer/ directory. (if it does not exist, pls create one)
	==> for using PIL, install pillow library with "pip install pillow"

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18   

'''

import cv2, os, numpy as np
from PIL import Image
from time import strftime

# Path for face image database
path = 'dataset'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

# function to get the images and label data
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    text = []

    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
        i = int(imagePath.split(".")[2])
        if(i == 1):
            face_id = int(imagePath.split(".")[1])
            text.append("{0}==={1}===Face<{0}>\n".format(face_id, strftime("%d-%m-%Y-%H-%M-%S")))

    return faceSamples, ids, text

print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces, ids, text = getImagesAndLabels(path)
open("trainer/Characters_Names.cn", "w").write("".join(text))
recognizer.train(faces, np.array(ids))

# Save the model into trainer/trainer.yml
if not os.path.exists("trainer/trainer.yml"):
    f = open("trainer/trainer.yml", "w")
    f.close()
recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi

# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
