from collections import defaultdict
# import cv2 as cv
import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image


# All the 6 methods for comparison in a list
# img1 = cv2.imread('./PNG/10.png')
# img2 = cv2.imread('./PNG/11.png')

img1 = cv2.imread('../video2/23.png')
img2 = cv2.imread('../video2/22.png')
# -2.8351473918188996

template = cv2.imread('../PNG/whitePic.png')

def calSim(input1, input2,dim = (500, 500)):
    print(input1.size)
    print(input2.shape)
    input1 = cv2.resize(input1, dim)
    input2 = cv2.resize(input2, dim)
    # input1 = cv2.cvtColor(input1, cv2.COLOR_BGR2GRAY)
    # input2 = cv2.cvtColor(input2, cv2.COLOR_BGR2GRAY)
    print(input1.shape)
    print(input2.shape)
    # cv2.imshow('Frame', input1)
    # cv2.waitKey()
    # cv2.imshow('Frame', input2)
    # cv2.waitKey()
    if input1.shape == input2.shape:
        errorL2 = cv2.norm(input1, input2, cv2.NORM_L2)
        similarity = 1 - errorL2 / (input1.shape[0] * input2.shape[1])
        return similarity
    return 0


print(calSim(img1,img2))
