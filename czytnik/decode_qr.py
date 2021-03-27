#!/usr/bin/env python3
import cv2
import time

detector = cv2.QRCodeDetector()

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    data, _, _ = detector.detectAndDecode(frame)
    cv2.imwrite('test.png', frame)
    print('image saved')
    if data:
        print('data found: ', data)
    time.sleep(0.5)

cap.release()
