# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import cv2
path = '../PNG\\'


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # construct the argument parser and parse the arguments

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--frames", type=int,default=100,help="frams in one second")
    # ap.add_argument("-v", "--video",help="path to the video file")
    ap.add_argument("-v", "--video",default = 'C:\\Users\\yizhe\\Videos\\Captures\\RAvideos\\RAvideo1.mp4',help="path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=800, help="minimum area size")
    #15
    args = vars(ap.parse_args())
    # if the video argument is None, then we are reading from webcam
    if args.get("video", None) is None:
        vs = VideoStream(src=0).start()
        time.sleep(2.0)

    # otherwise, we are reading from a video file
    else:
        vs = cv2.VideoCapture(args["video"])


    # initialize the first frame in the video stream
    c_ff = None
    left_part = None
    firstFrame = None
    count = 0
    # loop over the frames of the video
    f = 0
    s = set()
    total = 0
    sum_thresh = np.zeros((1000,950),dtype='int64')
    total_frames = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
    while f< total_frames:
        f +=1
        total_frames+=1
        # grab the current frame and initialize the occupied/unoccupied
        # text
        frame = vs.read()
        frame = frame if args.get("video", None) is None else frame[1]
        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
            break
        if f >= 600:
            count+=1
            # resize the frame, convert it to grayscale, and blur it
            cv2.imshow('Frame', frame)
            cv2.waitKey()
            frame = imutils.resize(frame, width=2000)
            cv2.imshow('Frame', frame)
            cv2.waitKey()
            # cv2.imshow('Frame', original_frame)
            # cv2.waitKey()
            original_frame = frame
            left_part = frame[:1000, 0:1050]
            frame = frame[:1000, 1050:]

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Frame', gray)
            cv2.waitKey()
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            if firstFrame is None:
                c_ff = frame
                firstFrame = gray
                # break
                continue
            if count == args["frames"]:
                frameDelta = cv2.absdiff(firstFrame, gray)
                # cv2.imshow('Frame', frameDelta)
                # cv2.waitKey()
                thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]
                total+=1
                sum_thresh += thresh
                count = 0
    print('out')
    sum_thresh = sum_thresh / total
    sum_thresh = sum_thresh.astype(np.uint8) #Convert to unit 8 pictures
    # cv2.imshow('Frame', sum_thresh)
    # cv2.waitKey()
    sum_thresh = cv2.threshold(sum_thresh, 200,255, cv2.THRESH_BINARY)[1]
    # cv2.imshow('Frame', sum_thresh)
    # cv2.waitKey()
    sum_thresh = cv2.dilate(sum_thresh, None, iterations=5)
    sum_thresh = sum_thresh.astype(np.uint8)
    # cv2.imshow('Frame', sum_thresh)
    # cv2.waitKey()
    cs = cv2.findContours(sum_thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cs = imutils.grab_contours(cs)
    idx = 0
    for c in cs:
        if cv2.contourArea(c) < args["min_area"]:
            continue
        (x, y, w, h) = cv2.boundingRect(c)
        roi = c_ff[y:y + h, x:x + w]
        frame = imutils.resize(roi, width=2000)
        # cv2.imshow('Frame', roi)
        # cv2.waitKey()
        cv2.imwrite(path+str(idx)+'.png', roi)
        cv2.rectangle(c_ff, (x, y), (x + w, y + h), (0, 255, 0), 2)
        idx+=1

    result = np.concatenate((left_part, c_ff), axis=1)
    cv2.imshow('Frame', result)
    cv2.waitKey()
    vs.stop() if args.get("video", None) is None else vs.release()
    cv2.destroyAllWindows()
