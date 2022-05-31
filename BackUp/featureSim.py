import cv2
import os

TARGET_FILE = '../images/pic6.png'
comparing_img_path = '../images/pic8.png'
IMG_SIZE = (500, 500)

target_img = cv2.imread(TARGET_FILE, cv2.IMREAD_GRAYSCALE)
target_img = cv2.resize(target_img, IMG_SIZE)

print(target_img.shape)
bf = cv2.BFMatcher(cv2.NORM_HAMMING)
detector = cv2.AKAZE_create()
(target_kp, target_des) = detector.detectAndCompute(target_img, None)
print("feature point: ", len(target_kp))

try:
    comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
    comparing_img = cv2.resize(comparing_img, IMG_SIZE)
    # cv2.imshow('Frame', comparing_img)
    # cv2.waitKey()
    (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
    matches = bf.match(target_des, comparing_des)
    dist = [m.distance for m in matches]
    ret = sum(dist) / len(dist)
except cv2.error:
    ret = 100000
# print(target_des)
# print(comparing_des)
print(ret)