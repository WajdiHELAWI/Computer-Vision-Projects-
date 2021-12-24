import cv2
import time
import os
import HandTrackingModule as htm


wCam, hCam = 640, 480 #640


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
# folderPath = "FingerImage"
# myList = os.listdir(folderPath)
# print(myList)
overlayList = []
# for imPath in myList:
#     image = cv2.imread(f'{folderPath}/{imPath}')
#     # print(f'{folderPath}/{imPath}')
#     overlayList.append(image)
# print(len(overlayList))
pTime = 0
detector = htm.handDetector(detectionCon=0.8)
tipIds = [4, 8, 12, 16, 20]
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
    if len(lmList) != 0:
        fingers = []
        # Thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(0,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
                
        totalFingers = fingers.count(1)
        # print(totalFingers)
        cv2.rectangle(img, (10, 10), (100, 100), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (10, 120), cv2.FONT_HERSHEY_PLAIN,10, (255, 0, 0), 10)
        
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)