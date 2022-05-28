import cv2
import numpy as np

img = cv2.imread("OpenCV/Resources/lena.png")
kernel = np.ones((5,5), np.uint8)

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(img, (5,5), 0)
imgCanny = cv2.Canny(img,150,200)
imgCannyBlur = cv2.Canny(imgBlur,150,200)

cv2.imshow("Gray Scale Image",imgGray)
cv2.imshow("Gaussian Blur Image",imgBlur)
cv2.imshow("Canny Image",imgCanny)
cv2.imshow("Canny on Blurred Image",imgCannyBlur)
cv2.waitKey(0)