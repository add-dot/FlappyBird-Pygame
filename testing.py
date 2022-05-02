import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#blue_lower = np.array([0, 55, 30])
#blue_upper = np.array([20, 255, 255])
blue_lower = np.array([95, 150, 30])
blue_upper = np.array([135, 255, 255])


while True:
    success, img = cap.read()
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, blue_lower, blue_upper)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours):
        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                M = cv2.moments(contour)
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
                print(cy)
                cv2.circle(img, (cx, cy), 5,(255, 255, 255), -1)
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)

    cv2.imshow("mask", mask)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
