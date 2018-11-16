import cv2
import numpy as np
from matplotlib import pyplot as plt
def nothing(x):
    pass
cv2.namedWindow('image')

cv2.createTrackbar('min','image',0,255,nothing)
cv2.createTrackbar('max','image',0,255,nothing)
cv2.createTrackbar('light','image',0,255,nothing)
img = cv2.imread('9.png',cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (640, 512), interpolation=cv2.INTER_CUBIC)

def _hough1(canny):
    global img
    hough = cv2.HoughLines(canny,1,np.pi/180,110)
    if hough is None:
        print('Hough without content')
        pass
    else:
        for i in range(len(hough)):
            for rho, theta in hough[i]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x2 = int(x0 - 300 * (-b))
                y2 = int(y0 - 300 * (a))
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
                cv2.imshow('houghlines3.jpg', img)


while(1):
    #l = cv2.getTrackbarPos('light','image')
    #img = np.uint8(np.clip((l + img), 0, 255))
    r = cv2.getTrackbarPos('min','image')
    g = cv2.getTrackbarPos('max','image')
    (T,edges) = cv2.threshold(img,r,g,cv2.THRESH_BINARY)



    canny = cv2.Canny(edges,50,150)
    cv2.imshow('image',canny)
    #_hough1(canny)
    k = cv2.waitKey(1)&0xFF
    if k == 27:
        break
    #r = cv2.getTrackbarPos('R','image')
    #g = cv2.getTrackbarPos('G','image')




cv2.destroyAllWindows()
cv2.waitKey(0)