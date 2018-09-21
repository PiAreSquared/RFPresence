#Created by Vishal Muthuraja
#12 September 2018


#import the necessary packages
import numpy as np
import argparse
import imutils
import cv2

#reads the images
img_rgb = cv2.imread('/home/vishal/Downloads/simpsons.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('/home/vishal/Downloads/barts_face.jpg',0)

#finds dimensions of the cropped image
w, h = template.shape[::-1]

#calculations to determine if cropped image is found in original image
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.6335
widthl=[];heightl=[]
loc = np.where( res >= threshold)

#for loop to determine all the coordinates
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    widthl.append(int(pt[0]+w))
    heightl.append(int(pt[1]+h))

#averages coordinates for a more accurate coordinate
height = str(int(sum(heightl) / float(len(heightl))))
width = str(int(sum(widthl) / float(len(widthl))))

#prints the coordinates
print("("+width+", "+height+")")
print("("+str(pt[0])+", "+height+")")
print("("+width+", "+str(pt[1])+")")
print("("+str(pt[0])+", "+str(pt[1])+")")


#boxes the detected cropped image in the original image
cv2.imshow('Detected',img_rgb)
cv2.waitKey(0)
cv2.imwrite('detectedimg.png',img_rgb)
cv2.destroyAllWindows()
