#Mobile Object Detection and Tracking

import cv2
import numpy as np
#import RPi.GPIO as GPIO
#import time

#GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
global area

def pinset():
#Motor 1 Pins
	m1e1 = 4	#ENABLE
	m1in1= 5
	m1in2= 6
#Motor 2 Pins
	m2e1 = 14	#ENABLE
	m2in1= 15
	m2in2= 16


def setup():
	GPIO.setup(m1in1, GPIO.OUT)
	GPIO.setup(m1in2, GPIO.OUT)
	GPIO.setup(m1e1, GPIO.OUT)
	GPIO.setup(m2e1, GPIO.OUT)
	GPIO.setup(m2in1, GPIO.OUT)
	GPIO.setup(m2in2, GPIO.OUT)

	GPIO.output(m2e1, 1)
	GPIO.output(m2e1, 1)

def stop():
    GPIO.output(m1in1, 0)
    GPIO.output(m1in2, 0)
    GPIO.output(m2in1, 0)
    GPIO.output(m2in2, 0)

def left():
    GPIO.output(m1in1, 0)
    GPIO.output(m1in2, 1)
    GPIO.output(m2in1, 0)
    GPIO.output(m2in2, 0)

def right():
    GPIO.output(m1in1, 0)
    GPIO.output(m1in2, 0)
    GPIO.output(m2in1, 0)
    GPIO.output(m2in2, 1)

def forward():
    GPIO.output(m1in1, 0)
    GPIO.output(m1in2, 1)
    GPIO.output(m2in1, 0)
    GPIO.output(m2in2, 1)

def backward():
    GPIO.output(m1in1, 1)
    GPIO.output(m1in2, 0)
    GPIO.output(m2in1, 1)
    GPIO.output(m2in2, 0)

def diff_left():
    GPIO.output(m1in1, 1)
    GPIO.output(m1in2, 0)
    GPIO.output(m2in1, 0)
    GPIO.output(m2in2, 1)

def diff_right():
    GPIO.output(m1in1, 0)
    GPIO.output(m1in2, 1)
    GPIO.output(m2in1, 1)
    GPIO.output(m2in2, 0)

def back_right():
    GPIO.output(m1in1, 0)
    GPIO.output(m1in2, 0)
    GPIO.output(m2in1, 1)
    GPIO.output(m2in2, 0)

def back_left():
    GPIO.output(m1in1, 1)
    GPIO.output(m1in2, 0)
    GPIO.output(m2in1, 0)
    GPIO.output(m2in2, 0)

#DETECTION

while True:
	capture = cv2.VideoCapture(https://ipaddress, cv2.CAP_DSHOW); #Enter pi camera location
	capture.set(3, 480)		#Frame height and width
	capture.set(4, 640)

	_, frm = capture.read()

	rows, cols, _ = frm.shape

	#SETTING AXIS FOR HORIZONTAL TRACKING
	x_medium = int(cols / 2	)
	center = int(cols / 2)

	#gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)

	#DETECTING YELLOW
	hsv = cv2.cvtColor(frm, cv2.COLOR_BGR2HSV)
	lowb = np.array([20, 100, 100], dtype=np.uint8)
	highb = np.array([44, 255, 255], dtype=np.uint8)
	mask = cv2.inRange(hsv, lowb, highb)

	contours, heirachy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

	for cnt in contours:
		(x, y, w, h) = cv2.boundingRect(cnt)
		R = cv2.rectangle(frm, (x, y), (x + w, y + h), (0, 255, 0), 2) #Bounding Box

		x_medium = int((x + x + w) / 2) #Tracks only horizontal movement
		area = h*w
		break

	cv2.line(frm, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
	cv2.imshow("Mask", mask)
	cv2.imshow("Video", frm)
	#print(area)
	#print(x_medium)
	#print(center)

	if x_medium >=270 and x_medium <= 370 and area >=20000 and area <=25000:
		print("Stop")

	if x_medium >=270 and x_medium <= 370 and area <=20000:
		print("Foward")

	if x_medium >=270 and x_medium <= 370 and area >25000:
		print("Backward")

	if x_medium >370 and area >=20000 and area <=25000:
		print("Differential Right")

	if x_medium <270 and area >=20000 and area <=25000:
		print("Differential Left")

	if x_medium <270 and area <20000:
		print("Left")

	if x_medium >370 and area <20000:
		print("Right")

	if x_medium <270 and area >25000:
		print("Back Left")

	if x_medium >370 and area >25000:
		print("Back Right")

	key = cv2.waitKey(1)
	if key == 27: #ESC KEY
		break

capture.release()
cv2.destroyAllWindows()
