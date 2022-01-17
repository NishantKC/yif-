import cv2
import time
import numpy as np
#To save the output in a file output.avi
fourcc=cv2.VideoWriter_fourcc(*"XVID")
output=cv2.VideoWriter("output.avi",fourcc,20,(2000,2000))
#Starting the webcam
capture=cv2.VideoCapture(0)
#Allowing the webcam to start by making the code sleep for 2 seconds
time.sleep(2)
bg=0
#Capturing background for 60 frames
for i in range(60):
    ret,bg=capture.read()
#Flipping the background
bg= np.flip(bg,axis=1)
#Reading the captured frame until the camera is open
while (capture.isOpened()):
    ret,img=capture.read()
    if not ret:
        break
    #Flipping the image for consistency
    img= np.flip(img,axis=1)
    #Converting the color from BGR to HSV
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #Generating mask to detect red colour
    #These values can also be changed as per the color
    red1=np.array([0,120,50])
    red2=np.array([10,255,255])
    mask1=cv2.inRange(hsv,red1,red2)
    red3=np.array([170,120,50])
    red4=np.array([180,255,255])
    mask2=cv2.inRange(hsv,red3,red4)
    mask=mask1+mask2
    #Open and expand the image where there is mask 1 (color)
    mask1=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask1=cv2.morphologyEx(mask,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))
    #Selecting only the part that does not have mask one and saving in mask 2
    mask2=cv2.bitwise_not(mask1)
#Keeping only the part of the images without the red color 
    #(or any other color you may choose)
    res1=cv2.bitwise_and(img,img,mask=mask2)
    #Keeping only the part of the images with the red color
    #(or any other color you may choose)
    res2=cv2.bitwise_and(bg,bg,mask=mask1)
     #Generating the final output by merging res_1 and res_2
    output1=cv2.addWeighted(res1,1,res2,1,0)
    output.write(output1)
     #Displaying the output to the user
    cv2.imshow("magic",output1)
    cv2.waitKey(1)
capture.release()
cv2.destroyAllWindows()

