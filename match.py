import numpy as nm
import argparse
import imutils
import cv2
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--frame", required = True,
	help = "Path to the frame image")
ap.add_argument("-g", "--goal", required = True,
	help = "Path to the goal image")
args = vars(ap.parse_args())
goal = cv2.imread(args["goal"])
(goalHeight, goalWidth) = goal.shape[:2]
status = " No Target"
#frame = cv2.imread(args["frame"])
camera = cv2.VideoCapture(0)
camera.set(3,640)
camera.set(4,480)
while True:
	(grabbed, frame) = camera.read()
	frame = imutils.resize(frame, height = 640)

	result = cv2.matchTemplate(frame, goal, cv2.TM_CCOEFF)
	(_, _, minLoc, maxLoc) = cv2.minMaxLoc(result)
	center = (0,0)
	topLeft = maxLoc
	botRight = (topLeft[0] + goalWidth, topLeft[1] + goalHeight)
	roi = frame[topLeft[1]:botRight[1], topLeft[0]:botRight[0]]
	center = (topLeft[0] + goalWidth/2, topLeft[1] + goalHeight/2)
	print center
	if center > (0,0):
		status = "Targed detected @ "+ str(center)
	cv2.circle(frame, center, 25, (0, 0, 255), 4)
	#cv2.imwrite('output.png', imutils.resize(frame, height = 640))
	cv2.imshow("frame", frame)#, imutils.resize(frame,height  = 640))
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
        	break

