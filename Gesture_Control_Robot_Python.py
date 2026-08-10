import cv2
import mediapipe as mp
import serial
import time

ser = None
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    print("Serial Connected to Arduino on /dev/ttyACM0")
    time.sleep(2)
except Exception as e:
    print(f"WARNING: Could not connect to serial port: {e}")

mphands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.7
i

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Camera could not be accessed.")
    exit()

last_command = 'S'

def send_command(command, gesture_desc):
    global last_command
    if command != last_command:
        print(f"Sending Cmd: {command} ({gesture_desc})")
        if ser and ser.is_open:
            ser.write(command.encode())
        last_command = command

def get_finger_counts(hand_landmarks):
    lm = hand_landmarks.landmark
    finger_tips = [8, 12, 16, 20]
    fingers_open_close = []

    for tip_id in finger_tips:
        if lm[tip_id].y < lm[tip_id - 2].y:
            fingers_open_close.append(1)
        else:
            fingers_open_close.append(0)

    return fingers_open_close

print("Gesture Control Active. Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    command = 'S'
    gesture_name = "STOP"

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        finger_states = get_finger_counts(hand)

        if finger_states == [1, 0, 0, 0]:
            command = 'F'
            gesture_name = "FORWARD (1 Finger)"
        elif finger_states == [1, 1, 0, 0]:
            command = 'B'
            gesture_name = "BACKWARD (2 Fingers)"
        elif finger_states == [1, 1, 1, 1]:
            command = 'R'
            gesture_name = "RIGHT TURN (4 Fingers)"
        else:
            command = 'S'
            gesture_name = "STOP (Fist/Other)"
    else:
        command = 'S'
        gesture_name = "NO HAND (STOP)"

    send_command(command, gesture_name)

    cv2.putText(
        frame,
        f"CMD: {command} - {gesture_name}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Gesture Control Robot Interface", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

send_command('S', "Shutdown")
cap.release()
cv2.destroyAllWindows()
if ser and ser.is_open:
    ser.close()

print("Shutdown complete.")