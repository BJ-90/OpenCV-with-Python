import cv2
import math
import numpy as np
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
#################################################################

# Load Haar Cascade files
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
eyeCascade = cv2.CascadeClassifier("haarcascade_eye.xml")

# Turn on webCam
cap = cv2.VideoCapture(0)
cap.set(10, 150)

## cv2.CascadeClassifier.detectMultiScale(image[, scaleFactor[, minNeighbors[, flags[, minSize[, maxSize]]]]])
# scaleFactor: Parameter specifying how much the image size is reduced at each image scale.
# This scale factor is used to create scale pyramid as shown in the picture. Suppose, the scale factor is 1.03,
# it means we're using a small step for resizing, i.e. reduce size by 3 %, we increase the chance of a matching size
# with the model for detection is found, while it's expensive
## minNeighbors : Parameter specifying how many neighbors each candidate rectangle should have to retain it.
# This parameter will affect the quality of the detected faces: higher value results in less detections
# but with higher quality.

while True:
    ret, img = cap.read()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect Face
    faces = faceCascade.detectMultiScale(img_gray, 1.3, 5)
    # Draw Rectangle around the face
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255 ,0, 0), 2)
        # make sure detect eyes are withing face
        roi_gray = img_gray[y:y+h, x:x+w]
        roi_color = img[y:y + h, x:x + w]
        # Detect Eyes
        eyes = eyeCascade.detectMultiScale(roi_gray)
        # Draw Rectangle across eyes
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    # Output
    cv2.imshow("Image", img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:  # 27 is the number for Esc key
        break
cap.release()
cv2.destroyAllWindows



# img = cv2.imread("Faces.jpg")
# imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# faces = faceCascade.detectMultiScale(imgGray,1.01,15)
#
# # Create a box of detected faces
# for (x, y, w, h) in faces:
#     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 5)
#
# # Output
# Images = concat_tile_resize([[img]], 0.4)
# cv2.imshow("Faces", Images)
# cv2.waitKey(0)