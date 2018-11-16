import cv2
import numpy as np

scr = cv2.imread('../hori_check/img_data/p6.png')
h,w,d = np.array(scr).shape
scr = cv2.resize(scr,(int(h*0.3),int(w*0.3)))
scr2 = cv2.imread('../hori_check/img_data/p7.png')
h1,w1,d1 = np.array(scr2).shape
scr2 = cv2.resize(scr2,(int(h1*0.3),int(w1*0.3)))
#cv2.namedWindow('f1',cv2.WINDOW_AUTOSIZE)
#cv2.imshow('f1', scr)

def create_rgb_hist(img):
    h,w,c = img.shape
    rgbHist = np.zeros([16*16*16,1],np.float32)
    bsize = 256/16
    for row in range(h):
        for col in range(w):
            b = img[row,col,0]
            g = img[row,col,1]
            r = img[row,col,2]
            index = np.int(b/bsize)*16*16 + 16*np.int(g/bsize) +np.int(r/bsize)
            rgbHist[np.int(index),0] = rgbHist[np.int(index),0]+1
    return rgbHist

def hist_compare(img1,img2):
    hist1 = create_rgb_hist(img1)
    hist2 = create_rgb_hist(img2)
    match1 = cv2.compareHist(hist1,hist2,cv2.HISTCMP_BHATTACHARYYA)
    match2 = cv2.compareHist(hist1,hist2,cv2.HISTCMP_CORREL)
    match3 = cv2.compareHist(hist1,hist2,cv2.HISTCMP_CHISQR)
    print('巴士距离： %s, 相关性：%s， kafang: %s'%(match1,match2,match3))
    #print(match2)

print('------------')
hist_compare(scr,scr2)
cv2.waitKey(0)
