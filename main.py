import methods

def main():
	# Initialize variables
	detector, args, movinObject, compare_container, vs, firstFrame, framePassed, total_framePassed = methods.Initiallization()

	# Go through frames in the input video
	while True:
		# Read Frames
		frame, framePassed, total_framePassed = methods.readFrames(vs, args, framePassed, total_framePassed)

		# Start processing video after certain frame
		if total_framePassed >args['frameStarted']:

			# If video ends, stop
			if frame is None:
				break

			# turn frames into gray and blur it (reduce noise and computation)
			frame, gray = methods.grayAndBlur(frame)

			# Set the firstFrame
			if firstFrame is None:
				firstFrame = gray
				continue

			# After x frame passed, reset the firstFrame
			if framePassed == args['frames']:
				firstFrame = gray
				framePassed = 0
				continue

			# Find contour after we did image subtraction (currFrame - firstFrame)
			cnts = methods.findContour(firstFrame,gray,args)

			# Store it inside a container
			methods.storeDetectedMovingObjects(cnts, args, frame, detector, compare_container)

	print("Objects captured:", compare_container.total_num_pic)

	# Call the container to remove captured objects that are too similar
	methods.removeDuplicate(compare_container)

	print("Objects captured after duplicates removed:", compare_container.pure_num_pic)

	# Store it locally in your computer
	methods.store(compare_container, args)

main()