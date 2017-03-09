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
# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video",
#	help="path to the (optional) video file")
#ap.add_argument("-b", "--buffer", type=int, default=64,
#	help="max buffer size")
#args = vars(ap.parse_args())
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
#greenLower = (29, 86, 6)
#greenUpper = (64, 255, 255)
greenLower = np.array([75,100,100])
greenUpper = np.array([140,255,255])
#pts = deque(maxlen=args["buffer"])
# if a video path was not supplied, grab the reference
# to the webcam
#if not args.get("video", False):
camera = cv2.VideoCapture(0)
camera.set(3,640)
camera.set(3,480)
minlist=[]
print camera.get(cv2.CAP_PROP_FRAME_WIDTH)
print camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
#cv2.VideoCapture.set(CV_CAP_PROP_FPS, 30)
# otherwise, grab a reference to the video file
#else:
#	camera = cv2.VideoCapture(args["video"])
# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
#	if args.get("video") and not grabbed:
#		break
	# resize the frame, blur it, and convert it to the HSV
	# color space
#frame = imutils.resize(frame, width=600)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
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
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
#		c = max(cnts, key=cv2.contourArea)
#		((x, y), radius) = cv2.minEnclosingCircle(c)
#		M = cv2.moments(c)
#		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
#		# only proceed if the radius meets a minimum size
#		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
#			cv2.circle(frame, (int(x), int(y)), int(radius),
#				(0, 255, 255), 2)
#			cv2.circle(frame, center, 5, (0, 0, 255), -1)
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
	                #for cnt1 in cnts:
					(x1,y1,w1,h1) = cv2.boundingRect(cnt1)
					mindict['xcoord'], mindict['ycoord'], mindict['width'], mindict['height'] = cv2.boundingRect(cnt1)
					mindict['rank'] = abs((float(w1)/float(h1)) - .4)
					minlist.append(mindict)
				#print mindict
				#commented out code below, now using a list to get two best matches instead of looping to find one
				#if float(min) >= abs((float(w1)/float(h1)) - .4):
				#	min = abs((float(w1)/float(h1)) - .4)
				#	(v,b,n,m) = cv2.boundingRect(cnt1)
					#cv2.rectangle(frame, (v,b), (v+n,b+m), (0,255,0), 4)
					#print min
				#minlst=
		minlist = sorted(minlist, key=lambda x: x['rank'])
#		print minlist
		#print json.dumps(minlist, indent=2)
		#if len(minlist) > 0:
		#	cv2.rectangle(frame, (minlist[0]['xcoord'],minlist[0]['ycoord']), (minlist[0]['xcoord']+minlist[0]['width'],minlist[0]['ycoord']+minlist[0]['height']), (0,255,0), 4)
		if len(minlist) > 1:
			if minlist[0]['width']-10 <= minlist[1]['width'] <= minlist[0]['width'] + 10 and minlist[0]['height']-10 <= minlist[1]['height'] <= minlist[0]['height']+10:
				if minlist[0]['ycoord']-10 <= minlist[1]['ycoord'] <= minlist[0]['ycoord']+10:
				#if 1.45 <= float(abs(minlist[0]['xcoord'] - minlist[1]['xcoord']))/float(minlist[0]['width']) <= 1.95:
					cv2.rectangle(frame, (minlist[0]['xcoord'],minlist[0]['ycoord']), (minlist[0]['xcoord']+minlist[0]['width'],minlist[0]['ycoord']+minlist[0]['height']), (0,255,0), 4)
					cv2.rectangle(frame, (minlist[1]['xcoord'],minlist[1]['ycoord']), (minlist[1]['xcoord']+minlist[1]['width'],minlist[1]['ycoord']+minlist[1]['height']), (0,255,0), 4)
				###########################
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
				###########################
#		print minlist
		minlist=[]
			#(x,y,w,h) = ecv2.boundingRect(cnt)
	   	 	#cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 3)
			#if float(2.6) <= (float(w)/float(h)) <= float(2.9):
			#	print "locked"
			#	cv2.rectangle(frame, (x,y), (x+w,y+h), (255,255,0), 3)
	# update the points queue
#	pts.appendleft(center)
	# loop over the set of tracked points
#	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
#		if pts[i - 1] is None or pts[i] is None:
#			continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
#		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
#		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
