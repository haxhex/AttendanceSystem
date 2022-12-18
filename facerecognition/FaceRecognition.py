import torch
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image
import cv2

class FaceRecognition(object):
    
    def __init__(self,database,model,fcd):
        self.database = database
        self.model = model
        self.fcd = fcd
    
    def preprocess(self,frame):
        frame_copy = frame.copy()
        faces, probs, landmarks = self.fcd.detect(frame_copy)
        self.fcd._draw(frame,faces,probs,landmarks)
        
        frame_copy = np.array(frame_copy)
        final_faces = []
        # print('len faces :',len(faces))
        if len(faces) != 0:
            for face in faces:
                # print('face = ',face)
                x , y , w ,h = face
                # print('x , y , w ,h : ',x , y , w ,h)
                # print('frame type = ', type(frame_copy))
                # print('frame shape = ', frame_copy.shape)
                detected_face = frame_copy[int(y):int(y+h), int(x):int(x+w)]
                # print('detected face shape => ', detected_face.shape)
                img = cv2.resize(detected_face, (112,112))
                # cv2.imwrite("./face.jpg",img)
                # print('img type :' ,type(img))
                # print('img shape :' ,img.shape)
                img_pixels = image.img_to_array(img)
                img_pixels = np.expand_dims(img_pixels, axis = 0)
                img_pixels /= 255 #normalize input in [0, 1]
                final_faces.append(img_pixels)
        
        return final_faces
    
    def apply_model(self,frame):
        predicted = []
        faces = self.preprocess(frame)
        # print('prepocessed faced => ',faces)
        for face in faces:
            # print('processing => ',face)
            predicted.append(self.model.predict(face)[0])

        # print('predicted type = ',type(predicted))
        return predicted
    
    def similarity_check(self):
        pass