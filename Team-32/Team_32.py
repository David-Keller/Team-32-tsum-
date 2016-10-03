import cv2
import numpy as np

img = cv2.imread('tum.png',0)
img2 = img.copy()

#cv2.imshow('detected circles',img2)
#cv2.waitKey(0)


img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)


#this line is being honed in becuse it has to do with the criteria for detecting circles
circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,25,
                            param1=35,param2=20,minRadius=15,maxRadius=40)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',img)
cv2.waitKey(0)
cv2.destroyAllWindows()