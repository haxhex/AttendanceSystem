from FaceDetector import FaceDetector as fd
from FaceRecognition import FaceRecognition as fr
from PIL import Image
import numpy as np
import cv2
from facenet_pytorch import MTCNN
from arcface import ArcFace

from Data import DataCreator


def main():
    cap = cv2.VideoCapture(0)
    model = ArcFace.ArcFaceModel(112)
    mtcnn = MTCNN()
    fcd = fd(mtcnn)
    fcr = fr(model,fcd)
    Data = DataCreator('facerecognition/Database/train',fcr)
    # Data.trainData()
    db = Data.loadData()
    while True:
        ret, frame = cap.read()
    # frame = Image.open('facerecognition/img0.jpg')
    
        try:
            # detect face box, probability and landmarks
            image = Image.fromarray(frame)
    # new = fcd.run(frame)
    # cv2.imwrite('facerecognition/new.jpg',np.asarray(new))
    # print("applied model to frame => ",fcr.apply_model(frame))
    # print("It's similar to => ",fcr.similarity_check(frame,db,0.45))

            print("It's similar to => ",fcr.similarity_check(image,db,0.01))
            # print("applied model to frame => ",fcr.apply_model(image))
        except:
            pass

        # Show the frame
        cv2.imshow('Face Detection', np.asarray(image))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    


if __name__ == '__main__':
    main()