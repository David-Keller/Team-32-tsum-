import cv2
import numpy as np
import time
#import all user created functions and classes
from solveGraph import *
from findTsums import findTsums


cap = cv2.VideoCapture(0)
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
    im = frame[20:690,50:1220].copy() #the copy is so any manipulatons to frame dont show up on im
    im = np.rot90(im)
    tsumList = findTsums(im)

    solvedList = createMap(tsumList)
    #solvedList.node
    
    cv2.rectangle(frame, (50,20), (1220,690), (0,255,0), thickness=2, lineType=8, shift=0)

#    # Display the resulting frame
    cv2.imshow('frame',frame)
    #cv2.imshow('im', im)
    

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

