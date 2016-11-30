import cv2
import numpy as np

def colorfilter(colorChange, lower, upper, i1, i2):
    mask = cv2.inRange(colorChange,lower,upper)
    kernel = np.ones((4,4),np.uint8)
    errode = cv2.erode(mask,kernel, iterations = i1)
    errode = cv2.dilate(errode,kernel, iterations = i2)
    return errode

def screenCorrection(im):
    colorChange = im.copy()
    colorChange = cv2.cvtColor(colorChange,cv2.COLOR_BGR2HSV)
    Olower = np.array([10,100,100])
    Oupper = np.array([28,255,255])
    Blower = np.array([101,50,50])
    Bupper = np.array([119,255,255])
    #mask = cv2.inRange(colorChange,Blower,Bupper)
    #kernel = np.ones((4,4),np.uint8)
    #errode = cv2.erode(mask,kernel, iterations = 1)
    #errode = cv2.dilate(errode,kernel, iterations = 9)
    errode = colorfilter(colorChange,Blower, Bupper,1,9)
    im2, contours, hierarchy = cv2.findContours(errode.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    Oerrode = colorfilter(colorChange,Olower,Oupper,1,1)
    
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
    rect = []
    for i in contours:
        rect.append(cv2.boundingRect(i))
    greaterthan = []
    for i in rect:
        if(i[0] < x and i[3] >175):
            greaterthan.append(i)
   
    for i in greaterthan:
        cv2.rectangle(im,(i[0],i[1]), (i[0]+i[2], i[1]+i[3]),(200,255,0), 2) 
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