from compareContainer import compareContainer
import argparse
import os
import imutils
import cv2

parent_dir = "C:\\Users\\yizhe\\Desktop\\RA\\OpenCV"

# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--frames", type=int, default=16, help="frams in one second")
# ap.add_argument("-v", "--video",default = 'C:\\Users\\yizhe\\Videos\\Captures\\RAvideos\\RAvideo2.mp4',help="path to the video file")
# ap.add_argument("-a", "--min-area", type=int, default=1500, help="minimum area size")
# ap.add_argument("-m", "--max-area", type=int, default=2000, help="maximum area size")
# ap.add_argument("-s", "--simlarityThreshold", type=int, default=85, help="higher the threhold is higher the standard of pictures")
# ap.add_argument("-c", "--movingThreshold", type=int, default=25, help="higher the threhold is higher the standard of moving objects")
# ap.add_argument("-st", "--frameStarted", type=int, default=0, help="higher the threhold is lower the standard of pictures")
# ap.add_argument("-dm", "--detectMode", type=int, default=1, help="0 = compare pixels, 1 = compare features")
# ap.add_argument("-fmin", "--MinfeatureNum", type=int, default=2, help="used to detect distinct objects, i.e target")
# ap.add_argument("-fmax", "--MaxfeatureNum", type=int, default=20, help="used to detect distinct objects, i.e target")
# ap.add_argument("-stl", "--storeLocation", default=".\\video2\\", help="used to detect distinct objects, i.e target")

# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--frames", type=int, default=12, help="frams in one second")
# ap.add_argument("-v", "--video",default = 'C:\\Users\\yizhe\\Videos\\Captures\\RAvideos\\RAvideo3.mp4',help="path to the video file")
# ap.add_argument("-a", "--min-area", type=int, default=1000, help="minimum area size")
# ap.add_argument("-m", "--max-area", type=int, default=10000, help="maximum area size")
# ap.add_argument("-s", "--simlarityThreshold", type=int, default=0.9, help="higher the threhold is higher the standard of pictures")
# ap.add_argument("-c", "--movingThreshold", type=int, default=25, help="higher the threhold is higher the standard of moving objects")
# ap.add_argument("-st", "--frameStarted", type=int, default=0, help="higher the threhold is lower the standard of pictures")
# ap.add_argument("-dm", "--detectMode", type=int, default=0, help="0 = compare pixels, 1 = compare features")
# ap.add_argument("-fmin", "--MinfeatureNum", type=int, default=0, help="used to detect distinct objects, i.e target")
# ap.add_argument("-fmax", "--MaxfeatureNum", type=int, default=0, help="used to detect distinct objects, i.e target")
# ap.add_argument("-stl", "--storeLocation", default=".\\video3\\", help="used to detect distinct objects, i.e target")


#
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--frames", type=int, default=8, help="frams in one second")
ap.add_argument("-v", "--video",default = 'C:\\Users\\yizhe\\Videos\\Captures\\RAvideos\\RAvideo4.mp4',help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=1000, help="minimum area size")
ap.add_argument("-m", "--max-area", type=int, default=10000, help="maximum area size")
ap.add_argument("-s", "--simlarityThreshold", type=int, default=120, help="higher the threhold is higher the standard of similar pictures")
ap.add_argument("-c", "--movingThreshold", type=int, default=25, help="higher the threhold is higher the standard of moving objects")
ap.add_argument("-st", "--frameStarted", type=int, default=0, help="higher the threhold is lower the standard of pictures")
ap.add_argument("-dm", "--detectMode", type=int, default=1, help="0 = compare pixels, 1 = compare features")
ap.add_argument("-fmin", "--MinfeatureNum", type=int, default=50, help="used to detect distinct objects, i.e target")
ap.add_argument("-fmax", "--MaxfeatureNum", type=int, default=100000, help="used to detect distinct objects, i.e target")
ap.add_argument("-stl", "--storeLocation", default=".\\video4\\", help="used to detect distinct objects, i.e target")

# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--frames", type=int, default=32, help="frams in one second")
# ap.add_argument("-v", "--video",default = 'C:\\Users\\yizhe\\Videos\\Captures\\RAvideos\\RAvideo5.mp4',help="path to the video file")
# ap.add_argument("-a", "--min-area", type=int, default=1000, help="minimum area size")
# ap.add_argument("-m", "--max-area", type=int, default=5000, help="maximum area size")
# ap.add_argument("-s", "--simlarityThreshold", type=int, default=50, help="check the provided doc")
# ap.add_argument("-c", "--movingThreshold", type=int, default=90, help="check the provided doc")
# ap.add_argument("-st", "--frameStarted", type=int, default=0, help="check the provided doc")
# ap.add_argument("-dm", "--detectMode", type=int, default=1, help="0 = compare pixels, 1 = compare features")
# ap.add_argument("-fmin", "--MinfeatureNum", type=int, default=50, help="used to detect distinct objects, i.e target")
# ap.add_argument("-fmax", "--MaxfeatureNum", type=int, default=4000, help="used to detect distinct objects, i.e target")
# ap.add_argument("-stl", "--storeLocation", default="where do you want to store the output.")

def Initiallization():
	detector = cv2.AKAZE_create()
	args = vars(ap.parse_args())
	movinObject = None
	compare_container = compareContainer(args["simlarityThreshold"],args["detectMode"])
	vs = cv2.VideoCapture(args["video"])
	firstFrame = None
	framePassed = 0
	total_framePassed= 0
	try:
		directory = args['storeLocation']
		path = os.path.join(parent_dir, directory)
		os.mkdir(path)
		print("Directory '% s' created" % directory)
	except Exception:
		print(args['storeLocation'],'already exist')
	return detector,args,movinObject,compare_container,vs,firstFrame,framePassed,total_framePassed

def readFrames(vs,args,framePassed,total_framePassed):
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	framePassed += 1
	total_framePassed += 1
	return frame, framePassed,total_framePassed
def grayAndBlur(frame):
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	return frame, gray
def findContour(firstFrame,gray,args):
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, args['movingThreshold'], 255, cv2.THRESH_BINARY)[1]
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	return cnts
def storeDetectedMovingObjects(cnts,args,frame,detector,compare_container):
	for c in cnts:
		if cv2.contourArea(c) < args["min_area"] or cv2.contourArea(c) > args["max_area"]:
			continue
		(x, y, w, h) = cv2.boundingRect(c)
		movinObject = frame[y:y + h, x:x + w]
		target_img = cv2.resize(movinObject, (500, 500))
		target_img = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
		(target_kp, target_des) = detector.detectAndCompute(target_img, None)
		if movinObject.shape[0] != 0 and movinObject.shape[1] != 0:
			if movinObject.shape[0] > 20 and movinObject.shape[1] > 20:
				if len(target_kp) >= args['MinfeatureNum'] and len(target_kp) <= args['MaxfeatureNum']:
					movingObjectSize = str(movinObject.shape)
					compare_container.add(movingObjectSize, movinObject)
def removeDuplicate(compare_container):
	compare_container.remove_duplicate()
def store(compare_container,args):
	for index, pic in enumerate(compare_container.duplicatesRemoved[0:40]):
		filename = f'{args["storeLocation"]}{index}.png'
		cv2.imwrite(filename, pic)