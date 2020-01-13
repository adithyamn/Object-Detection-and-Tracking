#Object Detection and Tracking

import cv2
import numpy as np

while True:
	capture = cv2.VideoCapture(0);
	capture.set(3, 480)
	capture.set(4, 640)
	
	_, frm = capture.read()
	
	rows, cols, _ = frm.shape
	
	x_medium = int(cols / 2)

	#DETECTING YELLOW
	hsv = cv2.cvtColor(frm, cv2.COLOR_BGR2HSV)
	lowb = np.array([20, 100, 100], dtype=np.uint8) 
	highb = np.array([44, 255, 255], dtype=np.uint8)
	mask = cv2.inRange(hsv, lowb, highb)

	contours, heirachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

	for cnt in contours:
		(x, y, w, h) = cv2.boundingRect(cnt)
		x_medium = int((x + x + w) / 2) #Tracks only horizontal movement
		cv2.rectangle(frm, (x, y), (x + w, y + h), (0, 255, 0), 2)
		global area
		area = h*w
		break

	cv2.line(frm, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
	cv2.imshow("Mask", mask)
	cv2.imshow("Video", frm)
	print(area)
	
#Closing Code
	key = cv2.waitKey(1)
	if key == 27: #ESC KEY
		break
capture.release()
cv2.destroyAllWindows()