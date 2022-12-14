# from json.tool import main
# from unicodedata import name
import face_detector as fd
from PIL import Image,ImageDraw
import numpy as np
import cv2



def main():
    cap = cv2.VideoCapture(0)
    cap.set(3,500)
    cap.set(4,500)
    while True :
        isSuccess,frame = cap.read()
        if isSuccess:            
            try:
#                 image = Image.fromarray(frame[...,::-1]) #bgr to rgb
                image = Image.fromarray(frame)
                frame_draw = frame.copy()
                frame_draw = Image.fromarray(frame_draw)
                draw = ImageDraw.Draw(frame_draw)
                
                boxes,landmarks = fd.detect(image)

                for i in range (len(boxes)):
                    draw.rectangle(boxes[i].tolist(), outline=(255, 0, 0), width=6)
                
                
                # bboxes, faces = mtcnn.align_multi(image, conf.face_limit, conf.min_face_size)
                # bboxes = bboxes[:,:-1] #shape:[10,4],only keep 10 highest possibiity faces
                # bboxes = bboxes.astype(int)
                # bboxes = bboxes + [-1,-1,1,1] # personal choice    
                # results, score = learner.infer(conf, faces, targets, args.tta)
                # # print(score[0])
                # for idx,bbox in enumerate(bboxes):
                #     if args.score:
                #         frame = draw_box_name(bbox, names[results[idx] + 1] + '_{:.2f}'.format(score[idx]), frame)
                #     else:
                #         if float('{:.2f}'.format(score[idx])) > .98:
                #             name = names[0]
                #         else:    
                #             name = names[results[idx]+1]
                #         frame = draw_box_name(bbox, names[results[idx] + 1], frame)

                frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                cv2.imshow('Input', np.asarray(frame_draw))               
            except:
                cv2.imshow('Input', np.asarray(frame))
                # cap.release()   
            
            # cv2.imshow('Arc Face Recognizer', frame)


        if cv2.waitKey(1)&0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

main()