# import the necessary packages
from collections import deque
import numpy as np
#import argparse
import json
#import imutils
import cv2
# Import PWM library
import wiringpi2
OUTPUT=1
PIN_TO_PWM = 30
wiringpi2.wiringPiSetup()
wiringpi2.pinMode(PIN_TO_PWM,OUTPUT)
wiringpi2.digitalWrite(PIN_TO_PWM,1)
wiringpi2.softPwmCreate(PIN_TO_PWM,0,1023)
min=10000000000
#greenLower = (29, 86, 6)
#greenUpper = (64, 255, 255)
greenLower = np.array([75,100,100])
greenUpper = np.array([140,255,255])
camera = cv2.VideoCapture(0)
camera.set(3,640)
camera.set(3,480)
minlist=[]
print camera.get(cv2.CAP_PROP_FRAME_WIDTH)
print camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# iterate through contours
		for cnt1 in cnts:
			peri = cv2.arcLength(cnt1, True)
			approx = cv2.approxPolyDP(cnt1, 0.01 * peri, True)
			area = cv2.contourArea(cnt1)
			hullArea = cv2.contourArea(cv2.convexHull(cnt1))
			solidity = area / float(hullArea)
			keepSolidity = solidity > 0.9
			(x, y, w, h) = cv2.boundingRect(approx)
                        aspectRatio = float(w) / float(h)
                        keepAspectRatio = aspectRatio >= 0.3 and aspectRatio <= .5

			if keepSolidity and keepAspectRatio:
				if len(approx) >= 4 and len(approx) <= 6:
 			#i=0
					mindict={}
					(x1,y1,w1,h1) = cv2.boundingRect(cnt1)
					mindict['xcoord'], mindict['ycoord'], mindict['width'], mindict['height'] = cv2.boundingRect(cnt1)
					mindict['rank'] = abs((float(w1)/float(h1)) - .4)
					minlist.append(mindict)
		minlist = sorted(minlist, key=lambda x: x['rank'])
		#if len(minlist) > 0:
		#	cv2.rectangle(frame, (minlist[0]['xcoord'],minlist[0]['ycoord']), (minlist[0]['xcoord']+minlist[0]['width'],minlist[0]['ycoord']+minlist[0]['height']), (0,255,0), 4)
		if len(minlist) > 1:
			if minlist[0]['width']-10 <= minlist[1]['width'] <= minlist[0]['width'] + 10 and minlist[0]['height']-10 <= minlist[1]['height'] <= minlist[0]['height']+10:
				if minlist[0]['ycoord']-10 <= minlist[1]['ycoord'] <= minlist[0]['ycoord']+10:
				#if 1.45 <= float(abs(minlist[0]['xcoord'] - minlist[1]['xcoord']))/float(minlist[0]['width']) <= 1.95:
					cv2.rectangle(frame, (minlist[0]['xcoord'],minlist[0]['ycoord']), (minlist[0]['xcoord']+minlist[0]['width'],minlist[0]['ycoord']+minlist[0]['height']), (0,255,0), 4)
					cv2.rectangle(frame, (minlist[1]['xcoord'],minlist[1]['ycoord']), (minlist[1]['xcoord']+minlist[1]['width'],minlist[1]['ycoord']+minlist[1]['height']), (0,255,0), 4)
					xwx=((float(minlist[0]['xcoord']+minlist[0]['width']) + float(minlist[1]['xcoord']))/2.0)
					wdth=(float(camera.get(cv2.CAP_PROP_FRAME_WIDTH))/2.0)
					print (wdth-xwx)*0.10375
					wiringpi2.softPwmWrite(PIN_TO_PWM,((float(1023)/float(640))*x))
					#if xwx <= wdth-5.0:
					#	print "Turn Left"
					#elif xwx >= wdth+5.0:
					#	print "Turn Right"
					#else:
					#	print "Centered"
		minlist=[]
			#(x,y,w,h) = ecv2.boundingRect(cnt)
	   	 	#cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 3)
			#if float(2.6) <= (float(w)/float(h)) <= float(2.9):
			#	print "locked"
			#	cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,0), 3)
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
