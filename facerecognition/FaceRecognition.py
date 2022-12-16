import torch
import numpy as np
from PIL import Image
import cv2

class FaceRecognition(object):
    
    def __init__(self,database,model,fcd):
        self.database = database
        self.model = model
        self.fcd = fcd
    
    def preprocess(self,frame):
        faces, probs, landmarks = fcd.detect(frame)
        print('h')
        final_faces = []
        if len(faces) != 0:
            for face in faces:
                x , y , w ,h = face
                detected_face = frame[int(y):int(y+h), int(x):int(x+w)]
                img = cv2.resize(detected_face, (112,112))
                img_pixels = detected_face.img_to_array(img)
                img_pixels = np.expand_dims(img_pixels, axis = 0)
                img_pixels /= 255 #normalize input in [0, 1]
                final_faces.append(img_pixels)
        
        return final_faces
    
    def apply_model(self,frame):
        print('hii')
        predected = []
        faces = self.preprocess(frame)
        for face in faces:
            predected.append(self.model.predect(face)[0])

        return predected
    
    def similarity_check(self):
        pass