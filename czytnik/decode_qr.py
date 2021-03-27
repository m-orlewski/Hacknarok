#!/usr/bin/env python3
import cv2
import time
import aes
import requests
from sys import argv

# example use: ./decode_qr.py http://hostname.domain

def request(data):
    print('GET',argv[1] + '/action?' + str(data, 'utf-8'))
    response = requests.get(argv[1] + '/action?' + str(data, 'utf-8'))

detector = cv2.QRCodeDetector()
cap = cv2.VideoCapture(0)

try: 
    while True:
        _, frame = cap.read()
        encrypted_data, _, _ = detector.detectAndDecode(frame)
    
        if encrypted_data:
            request(aes.decrypt(encrypted_data))
    
        time.sleep(0.5)

except KeyboardInterrupt:
    print('Keyboard interrupt recieved, stopping...')
    cap.release()
