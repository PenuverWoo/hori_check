import cv2
import numpy as np

img = '../hori_check/img_data/p20.png'

def cam_catch():
    cap = cv2.VideoCapture(1)
    while(1):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        cv2.imshow("capture", frame)
            #cv2.imshow('22',img)
        if cv2.waitKey(1) == ord('1'):
            cv2.imwrite(img,frame)
            # cv2.destroyAllWindows()
            break
    #cap.release()

def show():

    cv2.imshow('sss',cv2.imread(img))

def detect_img():
    d_img = cv2.imread(img,0)
    #d_img = cv2.cvtColor(d_img,cv2.COLOR_BGR2GRAY)
    ret,bin = cv2.threshold(d_img,200,50,cv2.THRESH_BINARY)
    cv2.imshow('ini_',bin)
    h,w = d_img.shape
    print(d_img.shap)
    print(d_img)
    # white = [255,255,255]
    # black = [0,0,0]
    # for i in range(h):
    #     for j in range(w):
    #         if white in d_img[i,j,:]:
    #             d_img[i,j,:] = white
    #         else:
    #             d_img[i,j,:] = black
    cv2.imshow('b_w',d_img)



cam_catch()
show()
# import sys
# import cv2 as cv
# import numpy as np
#
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
#
#
# class Video():
#     def __init__(self,capture):
#         self.capture = capture
#         self.currentFrame = np.array([])
#
#     def captureFrame(self):
#         ret, readFrame = self.capture.read()
#         return readFrame
#
#     def captureNextFrame(self):
#         ret, readFrame = self.capture.read()
#         if(ret == True):
#             self.currentFrame = cv.cvtColor(readFrame,cv.COLOR_BGR2GRAY)
#
#     def convertFrame(self):
#         try:
#             h,w, = self.currentFrame.shape[:2]
#             img = QImage(self.currentFrame,
#                          w,h, QImage.Format_RGB888)
#             img = QPixmap.fromImage(img)
#             self.previousFrame = self.currentFrame
#             return img
#         except:
#             return None
#
# class Gui(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setGeometry(250,80,800,600)
#         self.setWindowTitle('test')
#         self.video = Video(cv.VideoCapture(0))
#         self._timer = QTimer(self)
#         self._timer.timeout.connect(self.play)
#         self._timer.start(27)
#         self.update()
#         self.videoFrame = QLabel("VideoCapture")
#         self.videoFrame.setAlignment(Qt.AlignCenter)
#         self.setCentralWidget(self.videoFrame)
#
#         self.ret,self.capturedFrame = self.video.capture.read()
#
#     def play(self):
#         try:
#             self.video.captureNextFrame()
#             self.videoFrame.setPixmap(self.video.convertFrame())
#             self.videoFrame.setScaledContents(True)
#         except TypeError:
#             print('No Frane')
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ex = Gui()
#     ex.show()
#     sys.exit(app.exec_())