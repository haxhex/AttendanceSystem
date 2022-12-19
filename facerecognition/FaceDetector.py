import cv2
import numpy as np
from PIL import ImageDraw,Image


class FaceDetector(object):
    """
    Face detector class
    """

    def __init__(self, mtcnn):
        self.mtcnn = mtcnn
        self.detected = False

    def _draw(self, frame, boxes, probs, landmarks):
        """
        Draw landmarks and boxes for each face detected
        """
        try:
            draw = ImageDraw.Draw(frame)
            for box, prob, ld in zip(boxes, probs, landmarks):
                draw.rectangle(((box[0],box[1]),(box[2],box[3])),outline=(255,0,0),width=5)
                
                
                
        except:
            pass

        return frame
    
    def detect(self,frame):
        boxes, probs, landmarks = self.mtcnn.detect(frame, landmarks=True)
        if len(boxes) != 0 :
            self.detected = True
        return boxes, probs, landmarks


    def run(self,frame):
        """
            Run the FaceDetector and draw landmarks and boxes around detected faces
        """
        
        boxes, probs, landmarks = self.detect(frame)
        
        return self._draw(frame, boxes, probs, landmarks)
        
