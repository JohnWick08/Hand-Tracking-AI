#Gary Gao
#300124236

#reference https://stackoverflow.com/questions/30509573/writing-an-mp4-video-using-python-opencv
#https://stackoverflow.com/questions/66876906/create-a-rectangle-around-all-the-points-returned-from-mediapipe-hand-landmark-d
# read write video: https://learnopencv.com/reading-and-writing-videos-using-opencv/
# mediapipe https://google.github.io/mediapipe/solutions/hands.html
# draw dots https://stackoverflow.com/questions/49799057/how-to-draw-a-point-in-an-image-using-given-co-ordinate-with-python-opencv

import cv2
import mediapipe as mp

cap = cv2.VideoCapture('./videos_partA.mp4')


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

# Obtain frame size information using get() method
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width, frame_height)
fps = 10

# create a video writter
output = cv2.VideoWriter('./outputPartB.avi',
                         cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, frame_size)
#creates list
list = []

hands = mphands.Hands()

while (cap.isOpened()):
    data, image = cap.read()
    #print("hi")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    count = 0

    if results.multi_hand_landmarks:
        #for each hand
        for hand_landmarks in results.multi_hand_landmarks:
            count+=1
            colorChanger = 0
            if count==2:
                colorChanger=255
            h, w, c = image.shape

            # search for point 9 which is the center point of the hand
            for q, lm in enumerate(hand_landmarks.landmark):
                if q==9:
                    x, y = int(lm.x * w), int(lm.y * h)
                    i = 0
                    # changes color if it is the hand on the right
                    currentColor = (0, 0+colorChanger, 255-colorChanger)
                    #print(currentColor)
                    while i < len(list):
                        image = cv2.circle(
                            image, (list[i][0], list[i][1]), radius=0, color=list[i][2], thickness=10)
                        #draw dots and show
                        cv2.circle(image, (x, y), radius=0,
                                   color=list[i][2], thickness=10)
                        i += 1

                    #draw dots and save
                    image = cv2.circle(image, (x, y), radius=0,
                                    color=currentColor, thickness=10)

                    #add this dot into list
                    list.append([x, y,currentColor])

            if data == True:
                # Write the frame to the output files
                output.write(image)
            else:
                print("Stream disconnected")
                break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow('Handtracker', image)

# Release the video capture object
cv2.waitKey(0)
output.release()
cv2.destroyAllWindows()
