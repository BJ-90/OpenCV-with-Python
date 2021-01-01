import cv2

print("Package Imported")
# import image
img = cv2.imread("Lenna.png")
cv2.imshow("Output",img)
cv2.waitKey(0)

# import video
cap = cv2.VideoCapture("Frozen_Olaf.mp4")
while True:
    success, img = cap.read()
    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break

# access video cam
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)
while True:
    success, img = cap.read()
    cv2.imshow("Video",img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break