import cv2
from facerecognition.FaceDetector import FaceDetector
import cv2
import numpy as np
from PIL import ImageDraw,Image
from PIL import Image
import numpy as np
import cv2
from facenet_pytorch import MTCNN

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):

        mtcnn = MTCNN()
        fcd = FaceDetector(mtcnn)
        ret, frame = self.video.read()
        try:
            # detect face box, probability and landmarks
            image = Image.fromarray(frame)
            fcd.run(image)
            frame = np.array(image)
        except:
            pass
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')