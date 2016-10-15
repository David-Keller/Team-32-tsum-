# https://github.com/fireflyes/Team-32-tsum-
import cv2
import numpy as np
import time
#import all user created functions and classes
from solveGraph import *
from findTsums import findTsums
import ADBSwipe


imageSize = [720, 1280]
screenSize = ADBSwipe.getScreenSize()

cap = cv2.VideoCapture(1)
ret, frame = cap.read()
ret = cap.set(4,1080)
ret = cap.set(3,1920)
start = time.time()
seconds = 0.0
count = 0
while(True):
    end = start
    start = time.time()
    
    ret, frame = cap.read() 
    #frame = cv2.imread('test_data.png',1)
    im = frame[20:690,50:1220].copy() #the copy is so any manipulatons to frame dont show up in im
    im = np.rot90(im)
    tsumList = findTsums(im)
    if (tsumList is None):
        continue
    if(tsumList[0] is not None):
        length = len(tsumList[0])
        if(length > 3):
            print("found all 5")
#    print(tsumList[0])

    allTsums = list()
    for thisType in range(len(tsumList[0])):
        typeList = list()
        for j in tsumList[0][thisType]:
            thisTsum  = list()
            thisTsum.append(j[0])
            thisTsum.append(j[1])
            thisTsum.append(thisType)
            typeList.append(thisTsum)
        allTsums.append(typeList)
    myMap = NodeMap()
    myMap.createMap(allTsums)
    solvedList = myMap.getAllPaths()
    ADBSwipe.swipeTsumGroups(solvedList)
    print(solvedList)
    if(solvedList is not None):
        for path in solvedList:
            if(path is not None):
                for x in range(len(path)-1):
                    cv2.line(tsumList[1],(path[x].x,path[x].y),(path[x+1].x,path[x+1].y), (0,255,0),5)
    
    cv2.rectangle(frame, (50,20), (1220,690), (0,255,0), thickness=2, lineType=8, shift=0)

#    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow('im', tsumList[1])
    

    seconds = seconds +(start - end)
    count = count + 1
    if(seconds > 1):
        seconds = seconds - 1
        #print(count)
        count = 0
    if cv2.waitKey(200) & 0xFF == ord('q'):
        break

## When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

