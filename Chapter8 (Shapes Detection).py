import cv2
import numpy as np
import math

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

def getContour(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area < 30000:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 4)  # -1 means we want all shapes,(color),thickness)
            # Total length of each perimeter
            peri = cv2.arcLength(cnt, True)
            print(peri)
            # Total number corners of each shape
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            # print(approx) # Print position of each corner point
            print(len(approx))  # Total number of corner points in each shape
            objCor = len(approx)
            # Enclose and identify specific shapes
            x, y, w, h = cv2.boundingRect(approx)

            if objCor == 3: objectType = "Triangle"
            elif objCor == 4:
                aspRatio = w/float(h)
                if aspRatio > 0.95 and aspRatio < 1.05: objectType = "Square"
                else: objectType = "Rectangle"
            elif objCor > 4: objectType = "Circle"
            else: objectType = "None"

            cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0),1)
            cv2.putText(imgContour, objectType,
                        (x+(w//2)-10, y+(h//2)-10),
                        cv2.FONT_HERSHEY_COMPLEX, 1.4,
                        (0, 0, 0), 2)
##########################################################################

path = 'Shapes.png'
img = cv2.imread(path)
# Copy the image
imgContour = img.copy()

# Change to Grayscale image
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# print(imgGray.shape)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
# print(imgBlur.shape)
## find edges in our image
imgCanny = cv2.Canny(imgBlur,50,50)
getContour(imgCanny)

#############################################################
## Output
# Convert 1 array image into 3 array image
imgG = cv2.cvtColor(imgGray,cv2.COLOR_GRAY2BGR)
# print(imgG.shape)
imgB = cv2.cvtColor(imgBlur,cv2.COLOR_GRAY2BGR)
# print(imgB.shape)
imgC = cv2.cvtColor(imgCanny,cv2.COLOR_GRAY2BGR)

## Display Images
Images = concat_tile_resize([[img,imgG,imgB],
                             [imgC,imgContour]],0.7)
cv2.imshow("Stacked Image", Images)

cv2.waitKey(0)