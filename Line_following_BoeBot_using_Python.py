import numpy as np
import cv2
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
IN1=13
IN2=6
IN3=5

IN4=26
IN5=19
IN6=21


GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)

GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(IN5, GPIO.OUT)
GPIO.setup(IN6, GPIO.OUT)

cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)
while(cap.isOpened()):
    ret, frame = cap.read()
    crop_img = frame[60:120, 0:160]
    
    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret,thresh = cv2.threshold(blur,60,255,cv2.THRESH_BINARY_INV)
    imgs,contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
        cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
        cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
        if cx >= 120:
            print ("Turn Left!")
            
        if cx < 120 and cx > 50:
            print ("On Track!")
            GPIO.output(IN1,GPIO.HIGH)
            GPIO.output(IN2,GPIO.LOW)
            GPIO.output(IN3,GPIO.HIGH)
            GPIO.output(IN4,GPIO.HIGH)
            GPIO.output(IN5,GPIO.LOW)
            GPIO.output(IN6,GPIO.HIGH)
            sleep(0.2)
            GPIO.output(IN1,GPIO.LOW)
            GPIO.output(IN2,GPIO.LOW)
            GPIO.output(IN3,GPIO.LOW)
            GPIO.output(IN4,GPIO.LOW)
            GPIO.output(IN5,GPIO.LOW)
            GPIO.output(IN6,GPIO.LOW)
        if cx <= 50:
            print ("Turn Right")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        else:
            print ("i dont see the line")
            sleep(2)

        
    cv2.imshow('frame',crop_img)
