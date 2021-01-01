import cv2
import numpy as np

img = np.zeros((512,512,3),np.uint8)
# Add color to the image GBR
# img[:] = 255,0,0 # Blue image [height,width]
img[0:200,200:300] = 255,0,0

# Create line
cv2.line(img,(200,250),(512,512),(0,0,255),3) #(figure,st.point,end.point,color,thickness)
# Draw rectangle
# cv2.rectangle(img,(0,0),(100,190),(0,255,0),cv2.FILLED) #(img,st.point,end.point of diagnol, color,thickness/option)
cv2.rectangle(img,(0,0),(100,190),(0,255,0),2)
# Draw circle
cv2.circle(img,(300,200),30,(100,100,100),5) # (img,centre,radius,color,thickness)
# Add text
cv2.putText(img,"Open Sesomane",(100,350),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2) # (img,text,st.point,font,scale,color,thckness)
# Output
cv2.imshow("Image", img)

cv2.waitKey(0)