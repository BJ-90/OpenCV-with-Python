import cv2
import numpy as np

img = cv2.imread("Lenna.png")
# Find the size of the image
print(img.shape)
# Resize an Image
imgResize = cv2.resize(img,(300,400))

# Crop Image
imgCropped = img[0:200,200:400] #[height, width]

# Output
cv2.imshow("Image", img)
cv2.imshow("Image Resize", imgResize)
cv2.imshow("Cropped Resize", imgCropped)

cv2.waitKey(0)
