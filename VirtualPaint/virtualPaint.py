# VIRTUAL PAINT

import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

# [Hmin, Smin, Vmin, Hmax, Smax, Vmax]
myColors = [[110,51,0,130,255,255]] # Dark Blue

# [B, G, R]
myColorValues = [[78,4,4]] # Dark Blue

myPoints =  []  ## [x , y , colorId ]

# Paint brush thickness
thickness = 7

def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x, y = getContours(mask)
        cv2.circle(imgResult,(x,y),thickness,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count +=1
        #cv2.imshow(str(color[0]),mask)
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y = 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 400:
            cv2.drawContours(imgResult, cnt, -1, (255, 255, 255), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            rect = cv2.minAreaRect(approx)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            x = box[1][0]
            y = box[1][1]
            # cx, cy = int(rect[0][0]), int(rect[0][1])
            # w, h = int(rect[1][0]), int(rect[1][1])
            # theta = rect[2]
            cv2.rectangle(imgResult,(box[0][0],box[0][1]),
                          (box[2][0],box[2][1]),(255,255,255),2)
    return x, y

# def drawOnCanvas(myPoints,myColorValues):
#     for point in myPoints:
#         cv2.circle(imgResult, (point[0], point[1]), thickness, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)
    # if len(newPoints)!=0:
    #     for newP in newPoints:
    #         myPoints.append(newP)
    # if len(myPoints)!=0:
    #     drawOnCanvas(myPoints,myColorValues)


    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break