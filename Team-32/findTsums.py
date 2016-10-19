# https://github.com/fireflyes/Team-32-tsum-
import cv2
import numpy as np
#import time

def findTsums( first ):
    hight, width = first.shape[:2]
    fx = 720/width
    fy = 1280/hight
    cv2.resize(first,None,fx = fx, fy = fy)

    img = first.copy()

    img3 = first.copy()
    #img = cv2.multiply(img,np.array([2.0]))

    img = cv2.medianBlur(img,5)
    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    #this line is being honed in becuse it has to do with the criteria for detecting circles
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,
                                param1=50,param2=12,minRadius=40,maxRadius=50)
    if(circles is  None):
        return None
    circles = np.uint32(np.around(circles.astype(np.double)))

    #cut down on the number of data sets to work with based on being out of bounds
    circle = []
    for i in circles[0,:]:
        if((i[1] > 300) and (i[1] < 1000) and not (i[0] < i[2])): #TODO: the 300 and 1000 will need to be found dynamicaly """ change this to set radus (i[2]) equal to distance from edge(i[0]) """
            circle.append(i)

    #grab the regons of interest
    roiFirst = []
    for i in circle[0:]:
        roiFirst.append(img3[i[1]-(i[2]-2):(i[1]+(i[2])-2), i[0]-(i[2]-2):(i[0]+(i[2]-2))])

#TODO: clean up this loop and combine it with the previous loop
    #put a black circle mask over the regons of interest
    #num = 0
    roi = []
    for i in roiFirst:

        height, width, depth = i.shape
        temp = np.zeros((height,width), np.uint8)
        
        cv2.circle(temp,(int(height/2),int(width/2)),int((height-1)/2),1,-1)
        roi.append(cv2.bitwise_and(i, i, mask=temp))


    #calculate histograms
    hist = []
    num = 0
    for i in roi:
        if(i is None):
        #    print("None error")
            continue
        temp = cv2.calcHist([i],[0,1,2], None,[8,8,8], [0,256,0,256,0,256])
        hist.append((cv2.normalize(temp, temp).flatten(),num))
        num = num +1

    #histogram comparason and then sorting
    types = []
    if(len(hist)>0):
        types.append([hist[0]])
        for i in hist[1:]:
            found = False
            for j in types:
                temp = cv2.compareHist(i[0],j[0][0],method=0)
                if(temp > .85):## this is the value that determins how close the histograms have to be
                    j.append(i)
                    found = True
                    break   
            if(found == False):
                types.append([i])

    types.append(None)



#TODO: remove any lists from types that are less than 3 in length
    if(types[0] != None):
        for i in types[0][:]:
            cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(255,0,0),2)
        if(types[1] != None):
            for i in types[1][:]:
                cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(255,0,128),2)
            if(types[2] != None):
                for i in types[2][:]:
                    cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(255,0,255),2)
                if(types[3] != None):
                    for i in types[3][:]:
                        cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(255,128,128),2)
                    if(types[4] != None):
                        for i in types[4][:]:
                            cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(0,65,128),2)
                        if(types[5] != None):
                            for i in types[5][:]:
                                cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(0,65,255),2)

    #for i in types[6][:]:
    #    cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(65,150,128),2)

    #for i in types[7][:]:
    #    cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(0,0,200),2)

    types = [x for x in types if(x != None) if len(x) > 3]
    for i in types:
        for j in range(len(i)):
            i[j] = circle[i[j][1]]


    cv2.imshow('contrast',img3)
    #first = img3.copy()
    cv2.waitKey(1)
    #print(str(len(types)))
    return [types, img3]