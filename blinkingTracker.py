'''
Object detection ("Ball tracking") with OpenCV
	Adapted from the original code developed by Adrian Rosebrock
	Visit original post: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
Developed by Marcelo Rovai - MJRoBot.org @ 7Feb2018 
'''

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
# colorLower = (49, 100, 100)
# colorUpper = (99, 255, 255)
colorLower = (0, 0, 240)
colorUpper = (255, 50, 255)
pts = deque(maxlen=args["buffer"])

gbuffer = deque(maxlen=25)
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break
 
	# resize the frame, inverted ("vertical flip" w/ 180degrees),
	# blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width=600)
	# frame = imutils.rotate(frame, angle=180)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
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
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		# if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			# cv2.circle(frame, (int(x), int(y)), int(radius),
			# 	(0, 255, 255), 2)
			# cv2.circle(frame, center, 5, (0, 0, 255), -1)
 
	# update the points queue
	pts.appendleft(center)


		# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			gbuffer.append(0)
			continue
		
		gbuffer.append(1)
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

	if len(gbuffer) >= 6:
		print(gbuffer)
		if gbuffer[-6] == 1 and gbuffer [-5] == 0 and gbuffer [-4] == 0 and gbuffer[-3] == 1 and gbuffer [-2] == 0 and gbuffer [-1] == 0:
			print("ALELUYA")
		if gbuffer[-6] == 1 and gbuffer [-5] == 1 and gbuffer [-4] == 0 and gbuffer[-3] == 1 and gbuffer [-2] == 1 and gbuffer [-1] == 0:
			print("GERONIMO") 
		if len(gbuffer) >= 20:
			gbuffer.popleft()
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()