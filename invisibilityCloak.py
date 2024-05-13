import cv2
import time
import numpy as np

#to save the output in a file, output.avi
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = cv2.VideoWriter('output.avi',fourcc,20,(640,480))

#starting a webcam
cap = cv2.VideoCapture()

#allow the webcam to start
time.sleep(2)
bg = 0

#capturing the background for 60 frames
for i in range(60):
    ret,bg = cap.read()

#flipping the background
bg = np.flip(bg,axis = 1)

#reading the capture frame until the camera is open
while(cap.isOpened()):
    ret,img = cap.read()
    if not ret:
        break

    #covert the color from rgb to hsv
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #genrate mass to detect red color
    lower_red = np.array([0,120,50])
    upper_red = np.array([10,255,255])
    mask_1 = cv2.inRange(hsv,lower_red,upper_red)

    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask_2 = cv2.inRange(hsv,lower_red,upper_red)

    mask_1 = mask_1+mask_2

    #opening and expanding the image
    mask_1 = cv2.morphologyEx(mask_1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask_1 = cv2.morphologyEx(mask_1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

    #selectng only the part that has been removed by mask1 and save it in mask2
    mask_2 = cv2.bitwise_not(mask_1)

    #keeping only the part of the images without the red color
    res_1 = cv2.bitwise_and(img,img,mask = mask_2)
    res_2 = cv2.bitwise_and(bg,bg,mask = mask_1)

    #generating the final output by merging res1 and res2
    final_output = cv2.addWeighted(res_1,1,res_2,1,0)
    output_file.write(final_output)

    #display the output to the user
    cv2.imshow("magic",final_output)
    cv2.waitKe(1)

cap.release()
out.release()
cv2.destroyAllWindows()