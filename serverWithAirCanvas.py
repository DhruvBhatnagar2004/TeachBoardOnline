# Server with air canvas 
import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import socket
import pickle
import struct

# Giving different arrays to handle colour points of different colour
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# The kernel to be used for dilation purpose
kernel = np.ones((5, 5), np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Here is code for Canvas setup
paintWindow = np.zeros((471, 636, 3)) + 255
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Function to draw rectangles and put text on both paintWindow and frame
def draw_buttons(window):
    window = cv2.rectangle(window, (40, 1), (140, 65), (0, 0, 0), 2)
    window = cv2.rectangle(window, (160, 1), (255, 65), (255, 0, 0), 2)
    window = cv2.rectangle(window, (275, 1), (370, 65), (0, 255, 0), 2)
    window = cv2.rectangle(window, (390, 1), (485, 65), (0, 0, 255), 2)
    window = cv2.rectangle(window, (505, 1), (600, 65), (0, 255, 255), 2)
    cv2.putText(window, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(window, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(window, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(window, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(window, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

draw_buttons(paintWindow)

# Function to get the local IP address
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# Get the server's IP address
host_ip = get_ip_address()
print(f"Server IP Address: {host_ip}")

# Configure the server's socket
port = 9999
socket_address = (host_ip, port)

ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser_sock.bind(socket_address)
ser_sock.listen(5)

print(f"Server is listening on {socket_address}")

# Initialize the webcam
cap = cv2.VideoCapture(0)
ret = True

while True:
    client, addr = ser_sock.accept()
    print(f"Connected to Client @ {addr}")

    while ret:
        # Read each frame from the webcam
        ret, frame = cap.read()

        x, y, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)

        frame_copy = frame.copy()
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        draw_buttons(frame)

        # Get hand landmark prediction
        result = hands.process(framergb)

        # post process the result
        if result.multi_hand_landmarks:
            landmarks = [[int(lm.x * 640), int(lm.y * 480)] for handslms in result.multi_hand_landmarks for lm in handslms.landmark]

            for handslms in result.multi_hand_landmarks:
                # Drawing landmarks on frames
                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
            fore_finger = (landmarks[8][0], landmarks[8][1])
            center = fore_finger
            thumb = (landmarks[4][0], landmarks[4][1])
            cv2.circle(frame, center, 3, (0, 255, 0), -1)
            if (thumb[1] - center[1] < 30):
                bpoints.append(deque(maxlen=512))
                blue_index += 1
                gpoints.append(deque(maxlen=512))
                green_index += 1
                rpoints.append(deque(maxlen=512))
                red_index += 1
                ypoints.append(deque(maxlen=512))
                yellow_index += 1

            elif center[1] <= 65:
                if 40 <= center[0] <= 140:  # Clear Button
                    bpoints = [deque(maxlen=512)]
                    gpoints = [deque(maxlen=512)]
                    rpoints = [deque(maxlen=512)]
                    ypoints = [deque(maxlen=512)]
                    blue_index = 0
                    green_index = 0
                    red_index = 0
                    yellow_index = 0

                    paintWindow[67:, :, :] = 255
                elif 160 <= center[0] <= 255:
                    colorIndex = 0  # Blue
                elif 275 <= center[0] <= 370:
                    colorIndex = 1  # Green
                elif 390 <= center[0] <= 485:
                    colorIndex = 2  # Red
                elif 505 <= center[0] <= 600:
                    colorIndex = 3  # Yellow
            else:
                if colorIndex == 0:
                    bpoints[blue_index].appendleft(center)
                elif colorIndex == 1:
                    gpoints[green_index].appendleft(center)
                elif colorIndex == 2:
                    rpoints[red_index].appendleft(center)
                elif colorIndex == 3:
                    ypoints[yellow_index].appendleft(center)
        else:
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1

        # Draw lines of all the colors on the canvas and frame
        points = [bpoints, gpoints, rpoints, ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    #cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)

        # Serialize the paintWindow and send it to the client
        paint_data = pickle.dumps(frame)
        message = struct.pack("Q", len(paint_data)) + paint_data
        client.sendall(message)

        cv2.imshow("Output", frame)
        #cv2.imshow("Paint", paintWindow)

        key = cv2.waitKey(1) & 0xff
        if key == ord('q'):
            break

    cap.release()
    client.close()

cv2.destroyAllWindows()
