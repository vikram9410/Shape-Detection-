
              ################## shape detection using opencv   ######################

import cv2
import numpy as np
import imutils
# # this function is for joining images
def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver



def getContours (img):
    contours,group=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>500:  # to remove noise from image
         cv2.drawContours(imgContour,cnt,-1,(255,0,0),3)
         pari=cv2.arcLength(cnt,True)

         approx=cv2.approxPolyDP(cnt,0.02*pari,True)
         objCor=len(approx)
         x,y,w,h=cv2.boundingRect(approx)
         if objCor==3: objectType = "  Tri"
         elif objCor==4:      #two case square and rectangle
             ratio=w/float(h)
             if ratio>0.95 and ratio<1.05:
                 objectType = "Square"
             else:
                 objectType = "Rectangle"

         elif objCor==8:
          objectType = "Circle"


         cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
         cv2.putText(imgContour,objectType,(x+(w//2)-40,y+(h//2)+10),cv2.FONT_ITALIC,0.7,(0,0,0),2)
path="resources/shape1.png"
img=cv2.imread(path)
imgContour=img.copy()
imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur=cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny=cv2.Canny(imgBlur,50,50)
imgBlank=np.zeros((512,512,3),np.uint8)
getContours(imgCanny)
imageStack=stackImages(0.35,([img,imgGray,imgBlur],[imgCanny,imgContour,imgBlank]))

cv2.imshow("output",imageStack)
cv2.waitKey(0)

width= 650
height=500

def getContours (img):
    biggest=np.array([])
    maxArea=0
    contours,group=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>6000:  # to remove noise from image
         cv2.drawContours(imgContour,cnt,-1,(0,255,0),3)
         pari=cv2.arcLength(cnt,True)
         approx=cv2.approxPolyDP(cnt,0.02*pari,True)
         print(len(approx))

         if area>maxArea and len(approx)==4:
             biggest=approx
             maxArea=area
   # print(biggest)
    return biggest


