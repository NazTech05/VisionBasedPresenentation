import os
import cv2
import numpy as np
from HandTrackingModule import HandDetector

# Variables
width, height = 1280, 720
folderPath = "Presentation3"
imgNumber = 0
hs, ws = int(120 * 1), int(213 * 1)
gestureThreshold = 200
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
# imgCurrent -> slide
annotations = [[]]
annotationNumber = 0
annotationStart = False

# Camera Setup
print('Setting up the camera')
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(3, height)

# Get the list of presentation images (sorted based on the length of the name)
pathImages = sorted(os.listdir(folderPath), key=len)
# print(pathImages)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    # Import images
    # (Put the names of images in the list, import on every iteration, so that every time its a new image & not the one we have drawn on)
    success, img = cap.read()
    img = cv2.flip(img, 1)  # 1 = Horizontal, 0 = Vertical
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    #slide = cv2.imread(pathFullImage)
    slide = cv2.resize(cv2.imread(pathFullImage), (1540, 785))  # Changed w=1920, h=1080

    # Detecting Hands ,  flipType=False
    hands, img = detector.findHands(img)

    # Draw the dividing line on our video image, width=0, height=gestureThreshold, align the camera to the center of your face
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 8)

    # Get the landmarks and fingers of hand, and to do all of this - buttonPressed should be False
    if hands and buttonPressed is False:
        hand = hands[0]  # Only one hand is being detected, so get its info

        # A function to check how many fingers are up
        fingers = detector.fingersUp(hand)

        # If our hand is above this line, then we are going to accept this gesture
        cx, cy = hand['center']

        # print(fingers)
        # Getting the index finger, lmlist is landmark list, point no 8 is the index finger
        lmList = hand['lmList']
        # lmList, bbox = detector.findPosition(img)


        # Scale and constrain values for easier drawing, converting lmlist value from one range to another range
        # [Video], [Slide]
        # xVal = int(np.interp(lmList[8][0], [width // 2, w], [0, width]))  # Change this value to the total width
        # yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))

        xVal = int(np.interp(lmList[8][0], [350, width], [0, width + 4500]))
        yVal = int(np.interp(lmList[8][1], [150, height], [0, height + 1350]))

        indexFinger = xVal, yVal
        #indexFinger = lmList[8][0], lmList[8][1]

        # If hand is at the height of the face
        if cy <= gestureThreshold:

            # Whenever a gesture is applied, then buttonPressed becomes true
            # Gesture 1 : Left Thumb - go left
            if fingers == [1, 0, 0, 0, 0]:
                annotationStart = False
                print('Left')
                if imgNumber > 0:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    annotationStart = False
                    imgNumber -= 1

            # Gesture 2 : Right Finger - go right
            if fingers == [0, 0, 0, 0, 1]:
                annotationStart = False
                print('Right')
                if imgNumber < len(pathImages) - 1:
                    buttonPressed = True
                    annotations = [[]]
                    annotationNumber = 0
                    annotationStart = False
                    imgNumber += 1

        # Gesture 3 : Show pointer (Out of the threshold line so that it draws wherever we go)
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(slide, indexFinger, 7, (0, 0, 255), cv2.FILLED)

        # Gesture 4 : Draw pointer (When we have only the index finger)
        if fingers == [0, 1, 0, 0, 0]:

            # A new annotation every time you try to draw
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])

            cv2.circle(slide, indexFinger, 7, (0, 0, 255), cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)

        # End the annotation if it is any other finger
        else:
            annotationStart = False

        # Gesture 5 : Erase
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                if annotationNumber >= 0:
                    annotations.pop(-1)
                    annotationNumber -= 1
                    buttonPressed = True

    else:
        annotationStart = False

    # Button Pressed Iterations - Adding delay and to accept another button pressed
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    # To Draw - Take all the points and draw lines between these points
    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(slide, annotations[i][j-1], annotations[i][j], (0,0,200), 7)

    # Adding webcam image on the slides
    imgSmall = cv2.resize(img, (ws, hs))

    # Place it on our slides (Top right corner)
    # This will give us the width and height of the slides
    h, w, _ = slide.shape
    # print('Height and width of slides', h, w)

    # Change the matrix to image small - overlay the matrix
    slide[0:hs, w - ws:w] = imgSmall

    cv2.imshow('Image', img)
    cv2.imshow('Slides', slide)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break









# Pointer Scaling
# Window
# Hand name
# Controlling PPT