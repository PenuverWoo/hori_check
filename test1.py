import imutils
import scipy.spatial
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
def nothing(x):
    pass
img1 = cv2.imread('../hori_check/img_data/p10.png')
img1 = cv2.resize(img1, (640, 512))
img = cv2.imread('../hori_check/img_data/p10.png' )
img = cv2.resize(img, (640, 512))

img = np.uint8(np.clip((1.1 * img + 25), 0, 255))
#cv2.imshow('h_l',img)
print(img)
height, width, depth = np.array(img).shape
print('-----------------------------1')
print(height,width,depth)

print('-----------------------------w')
white = [255, 255, 255]
black = [0, 0, 0]
blue = [0, 169, 157]
#print(img[1,1,:])
'''
for i in range(height):
    for j in range(width):
        if white in img[i,j,:]:
            #img[i, j, :] = white
            #print(img[i,j,:])
            pass
        else:
            #pass
            img[i, j, :] = black
#cv2.imshow('chy',img)
'''

#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, binary = cv2.threshold(img, 200, 50, cv2.THRESH_BINARY)
#print(binary)
# contours = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img1,-1,(0,0,255),3)
# cv2.imshow('img',img1)
# cv2.imshow('ss',binary)
'''
cnts = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(cnts)
cv2.imshow('img',gray)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
print(cnts)
c = sorted(cnts, key=cv2.contourArea, reverse=True)
for i in range(len(c) - 1):
    x, y, w, h = cv2.boundingRect(c[i + 1])
    img[y: (y + h), x: (x + w), :] = black
    cv2.rectangle(img.shape, (x, y), (x + w, y + h), (0, 255, 0), 2)
'''

#canny = cv2.Canny(img,200,222)used on half pavilion
canny = cv2.Canny( binary   ,80,150)
print(canny)
cv2.imshow('canny3',canny)
#hough transform
lines = cv2.HoughLinesP(canny,1 ,np.pi/180,100  ,minLineLength=180,maxLineGap=5)
lines1 = lines[:,0,:]#提取为二维
print(lines1)
for x1,y1,x2,y2 in lines1[:]:
    cv2.line(img1,(x1,y1),(x2,y2),(0,0,255),1)
cv2.imshow('final',img1)
if cv2.waitKey(0)==27:
    cv2.destroyAllWindows()



'''
hough = cv2.HoughLines(canny, 1,np.pi/180,100)#used on half pavilion can got 2 lines
# # used on bezel can got five lines
#print(hough)
if hough is None:
    print('GG')



for i in range(len(hough)):
    for rho,theta in hough[i]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 300*(-b))
        y1 = int(y0 + 300*(a))
        x2 = int(x0 - 300*(-b))
        y2 = int(y0 - 300*(a))
        cv2.line(img1,(x1,y1),(x2,y2),(0,0,255),1)
        cv2.imshow('houghlines3.jpg',img1)
'''







