import cv2
import numpy as np

img = cv2.imread('test1.png',1)
temp = cv2.waitKey(0)
img2 = img.copy()
img3 = img.copy()
img4 = img.copy()
cv2.imshow('detected circleees',img3)
#temp = cv2.waitKey(0)
img = cv2.multiply(img,np.array([2.0]))

#cv2.imshow('detected circles',img2)
#cv2.waitKey(0)


img = cv2.medianBlur(img,9)
img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
#this line is being honed in becuse it has to do with the criteria for detecting circles
circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,
                            param1=50,param2=12,minRadius=40,maxRadius=50)

circles = np.uint16(np.around(circles))


roi = []


for i in circles[0,:]:
    # draw the outer circle
    roi.append(img3[i[1]-(i[2]):(i[1]+(i[2])), i[0]-(i[2]):(i[0]+(i[2]))])
    #cv2.imshow('contrast',roi)
    
    cv2.circle(img3,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    #cv2.circle(img3,(i[0],i[1]),2,(0,0,255),3)
num = 0
for i in roi:
    height, width, depth = i.shape
    temp = np.zeros((height,width), np.uint8)
    cv2.circle(temp,(int(height/2),int(width/2)),int((height-1)/2),1,-1)
    masked_data = cv2.bitwise_and(i, i, mask=temp)
    cv2.imshow('test' + str(num),masked_data)
    num = num + 1
cv2.imshow('contrast',img3)

hist = []
#calculate histograms
for i in roi:
    temp = cv2.calcHist([i],[0,1,2], None,[8,8,8], [0,256,0,256,0,256])
    hist.append(cv2.normalize(temp, temp).flatten())





#continue code here







#img2 = cv2.medianBlur(img2,9)
#img2 = cv2.cvtColor(img2,cv2.COLOR_RGB2GRAY)


##this line is being honed in becuse it has to do with the criteria for detecting circles
#circles = cv2.HoughCircles(img2,cv2.HOUGH_GRADIENT,1,50,
#                            param1=50,param2=12,minRadius=40,maxRadius=50)

#circles = np.uint16(np.around(circles))
#for i in circles[0,:]:
#    # draw the outer circle
#    cv2.circle(img4,(i[0],i[1]),i[2],(0,255,0),2)
#    # draw the center of the circle
#    cv2.circle(img4,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('regular',img4)
cv2.waitKey(0)
cv2.destroyAllWindows()



