import cv2
import numpy as np

############################################
# Combine images of different widths vertically
def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])), interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)
###########################################
# Combine images of different widths horizontally
def hconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(im.shape[0] for im in im_list)
    im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                      for im in im_list]
    return cv2.hconcat(im_list_resize)
###########################################
# Combine images of different sizes in vertical and horizontal tiles
def concat_tile_resize(im_list_2d, interpolation=cv2.INTER_CUBIC):
    im_list_v = [hconcat_resize_min(im_list_h, interpolation=cv2.INTER_CUBIC) for im_list_h in im_list_2d]
    return vconcat_resize_min(im_list_v, interpolation=cv2.INTER_CUBIC)
############################################

img1 = cv2.imread("Lenna.png")
img2 = cv2.imread("BD.jpg")

# Combine images of same width Horizontally
imgHor = np.hstack((img1,img1))
# Combine same image Horizontally
img_h = np.tile(img1, (1, 2, 1))
# Combine images of different widths horizontally
imgHorResize = hconcat_resize_min([img1, img2, img1])
# Combine images of same width Vertically
imgVer = np.vstack((img2,img2))
# Combine same image Vertically
img_v = np.tile(img2, (2, 1, 1))
# Combine images of different widths vertically
imgVerResize = vconcat_resize_min([img1, img2, img1])

# Combine images of different sizes in vertical and horizontal tiles
imgTiles = concat_tile_resize([[img1],
                                     [img1, img2, img1, img2, img1],
                                     [img1, img2, img1]])

# Output
cv2.imshow("Horizontal",imgHor)
cv2.imshow("Horizontal Image",img_h)
cv2.imshow("Multiple Horizontal Images",imgHorResize)
cv2.imshow("Vertical",imgVer)
cv2.imshow("Vertical Images",img_v)
cv2.imshow("Multiple Vertical Images",imgVerResize)

cv2.imshow("Multiple Images",imgTiles)

cv2.waitKey(0)

# Reference
# https://note.nkmk.me/en/python-opencv-hconcat-vconcat-np-tile/