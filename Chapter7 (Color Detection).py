import cv2
import numpy as np
import math
def empty(a):
    pass
###################################################################
# Combine images of different widths vertically
def vconcat_resize_min(im_list, scale, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    w_min1 = math.floor(w_min*scale)
    im_list_resize = [cv2.resize(im, (w_min1, int(im.shape[0] * w_min1 / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)
###########################################
# Combine images of different widths horizontally
def hconcat_resize_min(im_list, scale, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    h_min1 = math.floor(h_min*scale)
    # print(h_min1)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min1 / im.shape[0]), h_min1), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)
###########################################
# Combine images of different sizes in vertical and horizontal tiles
def concat_tile_resize(im_list_2d, scale, interpolation=cv2.INTER_CUBIC):
    im_list_v = [hconcat_resize_min(im_list_h, scale, interpolation=cv2.INTER_CUBIC) for im_list_h in im_list_2d]
    return vconcat_resize_min(im_list_v, scale, interpolation=cv2.INTER_CUBIC)
#####################################################################

path = 'BD.jpg'
# Create new window
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,250)
cv2.createTrackbar("Hue Min","TrackBars",159,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",179,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",122,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",255,255,empty)
cv2.createTrackbar("Val Min","TrackBars",59,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)

#####################################################
# while loop is used to extract color from original image
#while True:
img = cv2.imread(path)
imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
print(h_min,h_max,s_min,s_max,v_min,v_max)
##################################################

lower = np.array([h_min,s_min,v_min])
upper = np.array([h_max,s_max,v_max])
mask = cv2.inRange(imgHSV,lower,upper)
#print(mask.shape)
# mask is 1D array that can't be handle with cv2.hconcat
# Convert 1D (mask) to 3D (mask3D)
mask3D = cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
#print(mask3D.shape)
imgResult = cv2.bitwise_and(img,img,mask=mask)
#print(imgResult.shape)
##################################################

# Output
# cv2.imshow("Original",img)
# cv2.imshow("HSV",imgHSV)
# cv2.imshow("Mask", mask)
# cv2.imshow("Result", imgResult)

# Show all images in one window
imgStack = concat_tile_resize([[img,imgHSV],
                                 [mask3D,imgResult]],0.9)
cv2.imshow("Stacked Image", imgStack)
cv2.waitKey(0)