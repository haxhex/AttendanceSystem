from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
import numpy as np
import cv2
from PIL import Image, ImageDraw


device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))

def load_model():
    # detection_model = torch.load('./Models/detection/embeddings_all.pt')
    mtcnn = MTCNN(
        image_size=160, margin=0, min_face_size=20,
        thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
        device=device)
    return mtcnn

def detect(frame):
    mtcnn = load_model()
    boxes, _ = mtcnn.detect(frame)
    
    return boxes
