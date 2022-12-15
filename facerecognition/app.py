from FaceDetector import FaceDetector as fd

from facenet_pytorch import MTCNN


def main():
    mtcnn = MTCNN()
    fcd = fd(mtcnn)
    fcd.run()


if __name__ == '__main__':
    main()