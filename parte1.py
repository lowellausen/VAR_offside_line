import cv2
import sys

image = cv2.imread("maracana1.jpg")


cv2.imshow("OpenCV Image Reading", image)

cv2.waitKey(0)
