import matplotlib.pyplot as plt
import cv2

# source data
img_file = "target.png"

# create an OpenCV image
img = cv2.imread(img_file)

# convert color image to grey image
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

im_gauss = cv2.GaussianBlur(gray_img, (5, 5), 0)
ret, thresh = cv2.threshold(im_gauss, 150, 255, 0)
# cv2.imshow('Frame', thresh)
# cv2.waitKey()
# get contours
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
movinObject = 0
margin = 20
# calculate area and filter
for con in contours:
    area = cv2.contourArea(con)
    if 300 < area < 1000:
        x, y, w, h = cv2.boundingRect(con)
        # cv2.rectangle(img, (x - margin, y - margin), (x + w + margin, y + h + margin), (0, 255, 0), 2)
        movinObject = img[y-10:y + h + 13, x-25 :x + w + 25]
        break

cv2.imshow('Frame', movinObject)
cv2.waitKey()
filename = f'target2.png'
cv2.imwrite(filename, movinObject)
# plt.imshow(img, cmap='gray')