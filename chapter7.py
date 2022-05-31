import cv2
import numpy as np

# Input parameters
path = 'OpenCV/Resources/lambo.png'
TrackBars = 'TrackBars'
HueMin = 'HueMin'
HueMax = 'HueMax'
SatMin = 'SatMin'
SatMax = 'SatMax'
ValMin = 'ValMin'
ValMax = 'ValMax'

"""
This is a dummy callback function which gets called in createTrackbar method
"""
def empty(a):
    pass

"""
The main aim of this function is to stack images both horizontally and vertically

Inputs
======
Scale --> Scaling factor - Common for both x and y direction
imgArray --> Tuple of images ([I1, I2, I3], [I4, I5, I6])

Output (List of lists)
======================
+----+----+----+
| I1 | I2 | I3 |
+----+----+----+
| I4 | I5 | I6 |
+----+----+----+

Assumption: This function only processes the cases where input forms a
rectangular grid. For example, it cannot process for 'L' shape or 
inverted 'L' etc.

"""
def stackImages(scale,imgArray):
    # imgArray is a tuple

    # No. of rows and columns in imgArray
    rows = len(imgArray)
    cols = len(imgArray[0])

    # Check whether the input contains multiple rows
    # or a single row
    rowsAvailable = isinstance(imgArray[0], list)

    # Retrieve the width and height of the first image which will
    # act as a reference later  
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]

    # There are two different cases:
    # 1. Input contains multiple rows. 
    #    For eg. Input -> ([I1, I2], [I3, I4]), ([I1], [I2]) etc.
    # 2. Input contains a single row. 
    #    For eg. Input --> ([I1, I2]) etc.
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                # Resizing and Scaling
                # The first image is used as a reference.
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                # If the input image is in Gray scale format, convert it into BGR image
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        # Horizontal stacking of images
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        # Vertical stacking of images
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            # Resizing and Scaling
            # The first image is used as a reference.
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            # If the input image is in Gray scale format, convert it into BGR image
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        # Horizontal stacking of images
        hor= np.hstack(imgArray)
        ver = hor
    return ver




cv2.namedWindow(TrackBars)
cv2.resizeWindow(TrackBars,640,240)
cv2.createTrackbar(HueMin,TrackBars,0,179,empty)
cv2.createTrackbar(HueMax,TrackBars,19,179,empty)
cv2.createTrackbar(SatMin,TrackBars,110,255,empty)
cv2.createTrackbar(SatMax,TrackBars,240,255,empty)
cv2.createTrackbar(ValMin,TrackBars,153,255,empty)
cv2.createTrackbar(ValMax,TrackBars,255,255,empty)

while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos(HueMin, TrackBars)
    h_max = cv2.getTrackbarPos(HueMax, TrackBars)
    s_min = cv2.getTrackbarPos(SatMin, TrackBars)
    s_max = cv2.getTrackbarPos(SatMax, TrackBars)
    v_min = cv2.getTrackbarPos(ValMin, TrackBars)
    v_max = cv2.getTrackbarPos(ValMax, TrackBars)
    # Print and use the values to tune the mask
    # i.e. provide as an initial value
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)


    # cv2.imshow("Original",img)
    # cv2.imshow("HSV",imgHSV)
    # cv2.imshow("Mask", mask)
    # cv2.imshow("Result", imgResult)

    imgStack = stackImages(0.6,([img,imgHSV],[mask,imgResult]))
    cv2.imshow("Stacked Images", imgStack)

    cv2.waitKey(1)