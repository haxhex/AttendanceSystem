import cv2
import numpy as np
from PIL import ImageDraw,Image


class FaceDetector(object):
    """
    Face detector class
    """

    def __init__(self, mtcnn):
        self.mtcnn = mtcnn

    def _draw(self, frame, boxes, probs, landmarks):
        """
        Draw landmarks and boxes for each face detected
        """
        try:
            draw = ImageDraw.Draw(frame)
            for box, prob, ld in zip(boxes, probs, landmarks):
                draw.rectangle(((box[0],box[1]),(box[2],box[3])),outline=(255,0,0),width=5)
                
                draw.text((box[2],box[3]),str(prob))
                
        except:
            pass

        return frame
    def detect(self,frame):
        boxes, probs, landmarks = self.mtcnn.detect(frame, landmarks=True)
        return boxes, probs, landmarks


    def run(self):
        """
            Run the FaceDetector and draw landmarks and boxes around detected faces
        """
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            try:
                # detect face box, probability and landmarks
                
                # draw on frame
                image = Image.fromarray(frame)
                boxes, probs, landmarks = self.detect(image)
                
                frame_draw = frame.copy()
                frame_draw = Image.fromarray(frame_draw)

                self._draw(frame_draw, boxes, probs, landmarks)

            except:
                pass

            # Show the frame
            cv2.imshow('Face Detection', np.asarray(frame_draw))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        
