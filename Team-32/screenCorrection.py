import cv2
import numpy as np
# github link: 

def colorfilter(colorChange, lower, upper, i1, i2):
    mask = cv2.inRange(colorChange,lower,upper)
    kernel = np.ones((4,4),np.uint8)
    errode = cv2.erode(mask,kernel, iterations = i1)
    errode = cv2.dilate(errode,kernel, iterations = i2)
    mask = cv2.resize(mask,None,fx = .75, fy = .75)
    #cv2.imshow('mask',mask)
    return errode

def screenCorrection(im):
    ex = im.tolist()
    colorChange = im.copy()
    colorChange = cv2.cvtColor(colorChange,cv2.COLOR_BGR2HSV)
    Olower = np.array([16,200,200])
    Oupper = np.array([25,255,255])
    Blower = np.array([101,50,50])
    Bupper = np.array([119,255,255])
    Glower = np.array([30,100,100])
    Gupper = np.array([36,255,255])

    cv2.rectangle(im,(3,3), (4,3),(240,0,0), 2)



    greaterthan = []
    tempr = None
    templ = None
    tempg = None
    #mask = cv2.inRange(colorChange,Blower,Bupper)
    #kernel = np.ones((4,4),np.uint8)
    #errode = cv2.erode(mask,kernel, iterations = 1)
    #errode = cv2.dilate(errode,kernel, iterations = 9)
    errode = colorfilter(colorChange,Blower, Bupper,1,9)


    im2, contours, hierarchy = cv2.findContours(errode.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    
    areas = []
    num = 0
    for c in contours:
        area = cv2.contourArea(c)
        areas.append([area,num])
        num = num + 1
    areas.sort(key=lambda areas:areas[0], reverse=True)
    tec = contours[areas[0][1]]
    #im = cv2.drawContours(im,[tec],-1,(255,255,0),5)
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




    Oerrode = colorfilter(colorChange,Olower,Oupper,1,5)
    im2, Ocontours, hierarchy = cv2.findContours(Oerrode.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    Orect = []
    for j in Ocontours:
        Orect.append(cv2.boundingRect(j))
    if(len(Orect) > 0):
        templ = Orect[0]
        tempr = Orect[0]
        for i in Orect:
            if(i[0] <templ[0]):
                templ = i
            if(i[0]+i[2] > tempr[0]+ tempr[2]):
                tempr = i
            cv2.rectangle(im,(i[0],i[1]), (i[0]+i[2], i[1]+i[3]),(128,255,128), 2)

        cv2.rectangle(im,(templ[0],templ[1]), (templ[0]+templ[2], templ[1]+templ[3]),(0,255,200), 2)
        cv2.rectangle(im,(tempr[0],tempr[1]), (tempr[0]+tempr[2], tempr[1]+tempr[3]),(0,255,255), 2)


    Gerrode = colorfilter(colorChange,Glower, Gupper,1,1)
    im2, Gcontours, hierarchy = cv2.findContours(Gerrode.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    Grect = []
    for j in Gcontours:
        Grect.append(cv2.boundingRect(j))
    if(len(Grect) > 0):
        tempg = Grect[0]
        for i in Grect:
            if(i[0]+i[2] > tempg[0]+ tempg[2] ):
               tempg = i
       # cv2.rectangle(im,(i[0],i[1]), (i[0]+i[2], i[1]+i[3]),(255,255,128), 2)

        cv2.rectangle(im,(tempg[0],tempg[1]), (tempg[0]+tempg[2], tempg[1]+tempg[3]),(255,255,255), 5)
    #cv2.rectangle(im,(tempr[0],tempr[1]), (tempr[0]+tempr[2], tempr[1]+tempr[3]),(0,255,255), 2)

    

    errode = cv2.resize(errode,None,fx = .80, fy = .80)
    im = cv2.resize(im,None,fx = .75, fy = .75)

    cv2.imshow('before correction',im)
    #cv2.imshow('erode', errode)
   # cv2.imshow('oooo', Oerrode)
    cv2.imshow('ggggg', Gerrode)

    iscorrected = False
    if(len(greaterthan) > 0 and tempg != None and templ != None and tempr != None):
        fan = [tempr[0]+(tempr[2]/2),tempr[1]+(tempr[3]/2)]
        pause = [templ[0]+(templ[2]/2),templ[1]+(templ[3]/2)]
        tsum = [tempg[0]+(tempg[2]/2),tempg[1]+(tempg[3]/2)]
        score = [greaterthan[0][0]+(greaterthan[0][2]/2),greaterthan[0][1]+(greaterthan[0][3]/2)]

        pts1 = np.float32([pause,fan,tsum,score])
        pts2 = np.float32([[177,108],[1090,108],[1090,614],[177,365]])

        M = cv2.getPerspectiveTransform(pts1,pts2)
        correction = cv2.warpPerspective(im,M,(1280,720))
        iscorrected = True
        cv2.imshow('correction', correction)
        


    cv2.waitKey(1)
    #return [correction, isCorrected]





#coords are in greaterthan


cap = cv2.VideoCapture(0)
ret, frame = cap.read()
ret = cap.set(4,1080)
ret = cap.set(3,1920)
shouldtap = False

while(True):
    ret, frame = cap.read() 
    im = frame[20:690,50:1220].copy() #the copy is so any manipulatons to frame dont show up in im
    #im = np.rot90(im)
    screenCorrection(im)


im = cv2.imread('test_data.png',1)
screenCorrection(im)