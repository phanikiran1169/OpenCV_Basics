import cv2
import numpy as np

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


def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area>500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            # print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            # print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            if objCor ==3: objectType ="Tri"
            elif objCor == 4:
                aspRatio = w/float(h)
                if aspRatio >0.98 and aspRatio <1.03: objectType= "Square"
                else:objectType="Rectangle"
            elif objCor>4: objectType= "Circle"
            else:objectType="None"



            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(imgContour,objectType,
                        (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,
                        (0,0,0),2)




path = 'OpenCV/Resources/shapes.png'
img = cv2.imread(path)
imgContour = img.copy()

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny = cv2.Canny(imgBlur,50,50)
getContours(imgCanny)

imgBlank = np.zeros_like(img)
imgStack = stackImages(0.8,([img,imgGray,imgBlur],
                            [imgCanny,imgContour,imgBlank]))

cv2.imshow("Stack", imgStack)

cv2.waitKey(0)