import numpy as np
import cv2
import cvui

WINDOW_NAME = 'CVUI Test'

cvui.init(WINDOW_NAME)
frame = np.zeros((200, 400, 3), np.uint8)
img = '../hori_check/img_data/p20.png'
cap = cv2.VideoCapture( 1 )
checkboxState = [False]
while True:
    ret, frame1 = cap.read()
    frame[:] = (49, 52, 49)
    cvui.text(frame, 10, 15, 'Hello world!')

    # Update cvui internal stuff
    if(cvui.button(frame,40,40,'cam_catch')):
        print('laji ')

    print('------------')
    # Show window content
    cv2.imshow(WINDOW_NAME, frame)

    if cv2.waitKey(20) == 27:
        break