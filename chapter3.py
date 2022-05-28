import cv2
import numpy as np

img = cv2.imread("OpenCV/Resources/shapes.png")
print(img.shape)

imgResize = cv2.resize(img,(1154,1152))
print(imgResize.shape)

imgCropped = img[0:499,200:499]

cv2.imshow("Image",img)
cv2.imshow("Image Resize",imgResize)
cv2.imshow("Image Cropped",imgCropped)

cv2.waitKey(0)