import cv2
import time
import os
import hand_tracking_module as htm
import serial

serialcomm = serial.Serial('COM4',9600) 
serialcomm.timeout =2  

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

counter=0;
        
path="finger"
myList=os.listdir(path)
overlayList=[]

for impath in myList:
    image=cv2.imread(f'{path}/{impath}')
    overlayList.append(image)
pTime=0

detector=htm.handDetector(detectionCon=0.75)
tipIds=[4,8,12,16,20]
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    #print(lmList)
    if len(lmList) !=0:
        fingers=[]

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):  #y axis
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        totalFingers=fingers.count(1)

        counter+=1;
        if(counter>5):
                print(totalFingers)
                e='\n'
                serialcomm.write(str(totalFingers).encode()) 
                serialcomm.write(e.encode()) 
                counter=0
        
        
        #h,w,c=overlayList[totalFingers].shape
        #img[0:h,0:w]=overlayList[totalFingers]

        #cv2.rectangle(img,(20,225),(170,425),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(totalFingers),(20,375),cv2.FONT_HERSHEY_TRIPLEX,5,(255,0,0),10)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)