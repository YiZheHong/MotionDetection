# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-v", "--video", default='C:\\Users\\yizhe\\Videos\\Captures\\RAvideo.mp4',
                help="path to the video file")

ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
# otherwise, we are reading from a video file
else:
	vs = cv2.VideoCapture(args["video"])
# initialize the first frame in the video stream
firstFrame = None
# loop over the frames of the video
c = 0
while True:
    c+=1
    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame = vs.read()
    frame = frame if args.get("video", None) is None else frame[1]
    text = "Unoccupied"
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame is None:
        break
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue
    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    print(c)
    # if c > 300:
    #     cv2.imshow('Frame', frameDelta)
    #     cv2.waitKey()
    cv2.imshow('Frame', frameDelta)
    cv2.waitKey()
    # print(frameDelta)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow('Frame', thresh)
    # cv2.waitKey()
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image

    thresh = cv2.dilate(thresh, None, iterations=2)
    # cv2.imshow('Frame', thresh)
    # cv2.waitKey()
    # cv2.imshow('Frame', thresh)
    # cv2.waitKey()
    # cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    #     cv2.CHAIN_APPROX_SIMPLE)
    # cnts = imutils.grab_contours(cnts)
    # # loop over the contours
    # for c in cnts:
    #     # if the contour is too small, ignore it
    #     if cv2.contourArea(c) < args["min_area"]:
    #         continue
    #     # compute the bounding box for the contour, draw it on the frame,
    #     # and update the text
    #     (x, y, w, h) = cv2.boundingRect(c)
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #     text = "Occupied"