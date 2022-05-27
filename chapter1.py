import cv2

"""
# Read an image file
# Change the path accordingly
img = cv2.imread("OpenCV/Resources/lena.png")

cv2.imshow("Output", img)
cv2.waitKey(0)
"""

"""
# Read a video file
# Change the path accordingly
cap = cv2.VideoCapture("OpenCV/Resources/test_video.mp4")

while True:
    success, img = cap.read()
    cv2.imshow("Output", img)
    if cv2.waitKey(42) & 0xFF == ord('q'):
        break
        
"""
# Read from your webcam

frameWidth = 1280
frameHeight = 720

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

while True:
    success, img = cap.read()
    # img = cv2.resize(frameWidth, frameHeight)
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break