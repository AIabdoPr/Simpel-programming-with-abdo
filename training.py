import cv2, os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()

detector = cv2.CascadeClassifier(r"C:\Users\Abdo Programming\Documents\Python project\Classes\face.xml");


class getImagesAndLabels:
    def __init__(self, cam, path = "dataset"):
        if not(list(path)[-1] == "/" or list(path)[-1] == "\\"):
            path = "".join([path, "/"])
        self.assure_path_exists(path)
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
        faceSamples, img, ids = [], None, []
        i = 0
        font = cv2.FONT_HERSHEY_SIMPLEX
        for imagePath in imagePaths:
            if(imagePath.split(".")[-1] == "jpg"):
                PIL_img = Image.open(imagePath).convert('L')

                img_numpy = np.array(PIL_img,'uint8')

                _, cam_img = cam.read()

                id = int(imagePath.split('.')[1])
                print(id,' : ',imagePath)

                faces = detector.detectMultiScale(img_numpy)

                for (x,y,w,h) in faces:
                    img = img_numpy
                    faceSamples.append(img[y:y+h,x:x+w])

                    text = ["", "_", "__", "___", "___", " __", "  _"]
                    cv2.putText(cam_img, 'Loading Trainer Faces'+str(text[i]), (10,40), font, 1, (255,255,255), 3)
                    cv2.imshow("Adding faces to traning set...", cam_img)
                    ids.append(id)
                    cv2.waitKey(10)
                if(i == 6):i = 0
                else:i += 1

        cv2.destroyAllWindows()

        faces, gray = faceSamples, img[y:y+h,x:x+w]

        recognizer.train(faces, np.array(ids))
        self.assure_path_exists('trainer/')

        recognizer.save('trainer/trainer.yml')

    def assure_path_exists(self, path):
        self.dir = os.path.dirname(path)
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)