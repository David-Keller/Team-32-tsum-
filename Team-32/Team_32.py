import cv2
import numpy as np
import time

first = cv2.imread('test3.png',1)
start = time.time()
seconds = 0
count = 0
while(True):
    end = start
    start = time.time()
    img = first.copy()

    #temp = cv2.waitKey(0)
    #img2 = img.copy()
    img3 = img.copy()
    #img4 = img.copy()
    #cv2.imshow('detected circleees',img3)
    #temp = cv2.waitKey(0)
    #img = cv2.multiply(img,np.array([2.0]))
    img = cv2.medianBlur(img,3)


    #start = time.time()


    img = cv2.medianBlur(img,5)


    img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)


    #this line is being honed in becuse it has to do with the criteria for detecting circles
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,
                                param1=50,param2=12,minRadius=40,maxRadius=50)



    circles = np.uint16(np.around(circles))



    #cut down on the number of data sets to work with based on being out of bounds
    circle = []
    for i in circles[0,:]:
        if((i[1] > 300) and (i[1] < 1000)): #the 300 and 1000 will need to be found dynamicaly
            circle.append(i)




    roiFirst = []
    for i in circle[0:]:
        # draw the outer circle
   
        roiFirst.append(img3[i[1]-(i[2]-10):(i[1]+(i[2])-10), i[0]-(i[2]-10):(i[0]+(i[2]-10))])
        #cv2.imshow('contrast',roi)
    
        #cv2.circle(img3,(i[0],i[1]),i[2],(0,255,0),2)
        #cv2.imshow('contrast',img3)
        #cv2.waitKey(0)






    num = 0
    roi = []
    for i in roiFirst:
        height, width, depth = i.shape
        temp = np.zeros((height,width), np.uint8)
        cv2.circle(temp,(int(height/2),int(width/2)),int((height-1)/2),1,-1)
        roi.append(cv2.bitwise_and(i, i, mask=temp))
        #cv2.imshow('test' + str(num),masked_data)
        #num = num + 1
    #cv2.imshow('contrast',img3)





    hist = []
    #calculate histograms
    num = 0
    for i in roi:
        temp = cv2.calcHist([i],[0,1,2], None,[8,8,8], [0,256,0,256,0,256])
        hist.append((cv2.normalize(temp, temp).flatten(),num))
        num = num +1

    types = []
    types.append([hist[0]])
    for i in hist[1:]:
        found = False
        for j in types:
            temp = cv2.compareHist(i[0],j[0][0],method=0)
            if(temp > .8):## this is the value that determins how close the histograms have to be
                j.append(i)
                found = True
                break   
        if(found == False):
            types.append([i])
                

    #num = 1
    #for i in types[4]:
    #    cv2.imshow('test' + str(num),roi[i[1]])
    #    num = num + 1




    for i in types[0][:]:
        cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(255,0,0),2)

    for i in types[1][:]:
        cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(255,0,128),2)

    for i in types[2][:]:
        cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(255,0,255),2)

    for i in types[3][:]:
        cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(255,128,128),2)

    for i in types[4][:]:
        cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(0,65,128),2)

    for i in types[5][:]:
        cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(0,65,255),2)

    #for i in types[6][:]:
    #    cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(65,150,128),2)

    #for i in types[7][:]:
    #    cv2.circle(img3,(circle[i[1]][0],circle[i[1]][1]),circle[i[1]][2],(0,0,200),2)


    #end = time.time()
    #print(end - start)

    cv2.imshow('contrast',img3)
    seconds = seconds +(start - end)
    count = count + 1
    if(seconds > 1):
        seconds = seconds - 1
        print(count)
        count = 0
    cv2.waitKey(1)


cv2.destroyAllWindows()







#import numpy as np
#import cv2
#import time

#cap = cv2.VideoCapture(0)
#ret = cap.set(3,1280)
#print(ret)
#ret = cap.set(4,720)
#print(ret)
#seconds = 0
#count = 0
#start = time.time()
#while(True):
#    # Capture frame-by-frame
#    end = start
#    start = time.time()
    
#    ret, frame = cap.read()
#    #print(frame.shape[:2])
    
#    #frame = np.rot90(frame)

#    # Our operations on the frame come here
#   # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#    # Display the resulting frame
#    cv2.imshow('frame',frame)
    

#    seconds = seconds +(start - end)
#    count = count + 1
#    if(seconds > 1):
#        seconds = seconds - 1
#        print(count)
#        count = 0
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break

## When everything done, release the capture
#cap.release()
#cv2.destroyAllWindows()
