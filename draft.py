import cv2
import mediapipe as mp
import math
import numpy as np
import pyautogui as pag

#########################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 7

tipIds = [4, 8, 12, 16, 20]
#########################

plocX, plocY = 0, 0
clocX, clocY = 0, 0


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def findPosition(results, img, handNo=0,):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])

    return lmList

def fingersUp(lmList):
    fingers = []

    # Ensure the required landmarks exist in lmList
    if all(idx < len(lmList) for idx in tipIds):
        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
    else:
        # Not all required landmarks are detected
        fingers = [0, 0, 0, 0, 0]

    return fingers


def findDistance(lmList, p1, p2, img, draw=True,r=15, t=3):
    x1, y1 = lmList[p1][1:]
    x2, y2 = lmList[p2][1:]
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

    if draw:
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
        cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
    length = math.hypot(x2 - x1, y2 - y1)

    return length#, img, [x1, y1, x2, y2, cx, cy]


# For webcam input:
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

wScr, hScr = pag.size()

with mp_hands.Hands(model_complexity=1, min_detection_confidence=0.2, min_tracking_confidence=0.2) as hands:
  while cap.isOpened():
    success, image = cap.read()

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
    
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

    # 1. Find hand Landmarks
    lmList = findPosition(results, image)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

    # 3. Check which fingers are up
    fingers = fingersUp(lmList)

    cv2.rectangle(image, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    # 4. Only Index Finger : Moving Mode
    if fingers[1] == 1 and fingers[2] == 0:
        # 5. Convert Coordinates
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
        # 6. Smoothen Values
        clocX = plocX + (x3 - plocX) / smoothening
        clocY = plocY + (y3 - plocY) / smoothening
    
        # 7. Move Mouse
        pag.moveTo(wScr - clocX, clocY)
        cv2.circle(image, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        plocX, plocY = clocX, clocY

    # 8. Both Index and middle fingers are up : Clicking Mode
    if fingers[1] == 1 and fingers[2] == 1:
        # 9. Find distance between fingers
        length = findDistance(lmList, 8, 12, image)
        # 10. Click mouse if distance short
        if length < 40:
            pag.click()


    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()