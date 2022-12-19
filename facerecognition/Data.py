import json
import os
from tkinter.tix import Tree
from PIL import Image
import numpy as np
class DataCreator(object):
    
    def __init__(self,dataPath,fcr):
        self.dataPath = dataPath
        self.fcr = fcr
    
    

    def encode_from_file(self,path):
        encoded = []
        try:
            print(os.listdir(path))
            for img in os.listdir(path):
                print(path+'/'+img)
                frame = Image.open(path+'/'+img)
                encoded.append(self.fcr.apply_model(frame))
        except IndexError:
            os.remove(path+'/'+img)
        return encoded

    def dataset_load_from_file(self):
        #path refers to train dir
        dataset = {}
        names = os.listdir(self.dataPath)
        for name in names:
            img = self.dataPath +'/'+name
            dataset[name] = self.encode_from_file(img)
            each_person_number = len(os.listdir(img))
            print(name+"'s total photo number = "+ str(each_person_number))
        return dataset
    
    def trainData(self):
        data = self.dataset_load_from_file()
        np.save('facerecognition/Database/data.npy', data)
         
    def loadData(self):
        return np.load('facerecognition/Database/data.npy',allow_pickle=True).item()
    

   