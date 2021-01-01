import cv2
import numpy as np

img = cv2.imread("BD.jpg")

width,height = 400,600
pts1 = np.float32([[540,30],[120,30],[120,360],[540,360]])
pts2 = np.float32([[width,height],[width,0],[0,0],[0,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
imgOutput = cv2.warpPerspective(img,matrix,(width,height))


# Output
cv2.imshow("Image",img)
cv2.imshow("Output",imgOutput)
cv2.waitKey(0)