#Gary Gao
#300124236
#reference https://stackoverflow.com/questions/30509573/writing-an-mp4-video-using-python-opencv
#https://stackoverflow.com/questions/66876906/create-a-rectangle-around-all-the-points-returned-from-mediapipe-hand-landmark-d
# read write video: https://learnopencv.com/reading-and-writing-videos-using-opencv/
# mediapipe https://google.github.io/mediapipe/solutions/hands.html
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

# Obtain frame size information using get() method
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width, frame_height)
fps = 10

# create a video writter
output = cv2.VideoWriter('./outputPartA.avi',
                         cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, frame_size)


hands = mphands.Hands()

while (cap.isOpened()):
    data, image = cap.read()
    #print("hi")

    # flip image and convert to RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # process imagee
    results = hands.process(image)
    # convert color
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if results.multi_hand_landmarks:

        # for each hand
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, c = image.shape
            x_max = 0
            y_max = 0
            x_min = w
            y_min = h

            # for each landmark, get the x_max,x_min,y_max,y_min
            for lm in hand_landmarks.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y

            # draw rectangles
            cv2.rectangle(image, (x_min, y_min),(x_max, y_max), (0, 255, 0), 2)
            #draw the hand 
            mp_drawing.draw_landmarks(image, hand_landmarks, mphands.HAND_CONNECTIONS)
            if data == True:
                # Write the frame to the output files
                output.write(image)
            else:
                print("Stream disconnected")
                break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow('Handtracker', image)
    cv2.waitKey(1)

# Release the video capture object
cv2.waitKey(0)
output.release()
cv2.destroyAllWindows()
