''''
Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
	==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
	==> Each face will have a unique numeric integer ID as 1, 2, 3, etc                       

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18    

'''

import cv2
import os

cam = cv2.VideoCapture(0)
# cam = cv2.VideoCapture("Now You See Me 2.wmv")
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
cam.set(1, 14000) 

if not os.path.exists("dataset"):
    os.system('md "dataset"')

if not os.path.exists("trainer"):
    os.system('md "trainer"')

font = cv2.FONT_HERSHEY_SIMPLEX

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0
i = 0
while(True):
    ret, img = cam.read();
    i = i+1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    imagePaths = [os.path.join("dataset",f) for f in os.listdir("dataset")]
    num = len(imagePaths)

    if not(num == 0):
        if(count == 0):
            face_id = str(int(imagePaths[-1].split(".")[1])+1)
    elif(num == 0 & count == 0):
        face_id = 0

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

        if(cv2.waitKey(10) & 0xff == ord("a")):
                if(count<50):
                    count += 1
                    cv2.putText(img, '{}%'.format(count*2), (x+10,h+5), font, 1, (255,255,0), 2)
                    # Save the captured image into the datasets folder
                    cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
                else:
                    cv2.destroyAllWindows()
                    count = 0

    cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()