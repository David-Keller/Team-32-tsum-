import cv2
import numpy as np

def screenCorrection(im):
    colorChange = im.copy()
    colorChange = cv2.cvtColor(colorChange,cv2.COLOR_BGR2HSV)
    #lower = np.array([10,100,100])
    #upper = np.array([28,255,255])
    lower = np.array([100,50,50])
    upper = np.array([120,255,255])
    mask = cv2.inRange(colorChange,lower,upper)
    kernel = np.ones((4,4),np.uint8)
    errode = cv2.erode(mask,kernel, iterations = 1)
    errode = cv2.dilate(errode,kernel, iterations = 8)
    im2, contours, hierarchy = cv2.findContours(errode.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    areas = []
    num = 0
    for c in contours:
        area = cv2.contourArea(c)
        areas.append([area,num])
        num = num + 1
    areas.sort(key=lambda areas:areas[0], reverse=True)
    tec = contours[areas[0][1]]
    im = cv2.drawContours(im,[tec],-1,(255,255,0),5)
    #im = cv2.drawContours(im,[contours[areas[2][1]]],-1,(255,127,0),5)
    x,y,w,h = cv2.boundingRect(tec)
    cv2.rectangle(im,(x,y), (x+w, y+h),(0,255,0), 2)
    
    #rect = cv2.minAreaRect(tec)
    #box = cv2.boxPoints(rect)
    #box = np.int0(box)
    #cv2.drawContours(im,[box],0,(0,0,255),2)

    errode = cv2.resize(errode,None,fx = .80, fy = .80)
    im = cv2.resize(im,None,fx = .75, fy = .75)
    mask = cv2.resize(mask,None,fx = .75, fy = .75)
    cv2.imshow('correction',im)
    cv2.imshow('mask',mask)
    cv2.imshow('erode', errode)
    cv2.waitKey(0)


im = cv2.imread('test_data.png',1)
screenCorrection(im)