import cv2
import mediapipe as mp
import pyautogui
import time

pyautogui.PAUSE = 0

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
mp_draw = mp.solutions.drawing_utils

# Visual mouse kanan bawah
mouse_x, mouse_y = 1000, 200
mouse_w, mouse_h = 150, 280

scroll_up_area = (mouse_x + 60, mouse_y + 70, mouse_x + 90, mouse_y + 110)
scroll_down_area = (mouse_x + 60, mouse_y + 160, mouse_x + 90, mouse_y + 200)
click_left_area = (mouse_x, mouse_y, mouse_x + 70, mouse_y + 120)
click_right_area = (mouse_x + 80, mouse_y, mouse_x + 150, mouse_y + 120)

# Keyboard kiri bawah
keyboard_x, keyboard_y = 50, 450
key_w, key_h, key_gap = 55, 55, 10

keys_row1 = list("QWERTYUIOP")
keys_row2 = list("ASDFGHJKL")
keys_row3 = list("ZXCVBNM")
special_keys = ["SPACE", "BACK"]

typed_text = ""

# Tahan jari start timer untuk debounce
hold_start_time = None
hold_area = None
hold_key = None

DEBOUNCE_HOLD_SEC = 1.0

def point_in_rect(x, y, rect):
    x1, y1, x2, y2 = rect
    return x1 <= x <= x2 and y1 <= y <= y2

def draw_ui(frame, highlight=None):
    if highlight is None:
        highlight = {}

    # Mouse body
    cv2.rectangle(frame, (mouse_x, mouse_y), (mouse_x+mouse_w, mouse_y+mouse_h), (150,150,150), -1)

    # Scroll up
    color_scroll_up = (100,100,100)
    if highlight.get('scroll_up'):
        color_scroll_up = (255, 0, 0)
    cv2.rectangle(frame, (scroll_up_area[0], scroll_up_area[1]), (scroll_up_area[2], scroll_up_area[3]), color_scroll_up, -1)
    cv2.putText(frame, "↑", (scroll_up_area[0]+8, scroll_up_area[3]-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)

    # Scroll down
    color_scroll_down = (100,100,100)
    if highlight.get('scroll_down'):
        color_scroll_down = (255, 0, 0)
    cv2.rectangle(frame, (scroll_down_area[0], scroll_down_area[1]), (scroll_down_area[2], scroll_down_area[3]), color_scroll_down, -1)
    cv2.putText(frame, "↓", (scroll_down_area[0]+8, scroll_down_area[3]-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)

    # Klik kiri
    color_left = (100,100,100)
    if highlight.get('left'):
        color_left = (0, 255, 0)
    cv2.rectangle(frame, (click_left_area[0], click_left_area[1]), (click_left_area[2], click_left_area[3]), color_left, -1)
    cv2.putText(frame, "L", (click_left_area[0]+20, click_left_area[1]+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)

    # Klik kanan
    color_right = (100,100,100)
    if highlight.get('right'):
        color_right = (0, 0, 255)
    cv2.rectangle(frame, (click_right_area[0], click_right_area[1]), (click_right_area[2], click_right_area[3]), color_right, -1)
    cv2.putText(frame, "R", (click_right_area[0]+20, click_right_area[1]+80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)

    # Keyboard
    # Baris 1
    for i, k in enumerate(keys_row1):
        x = keyboard_x + i * (key_w + key_gap)
        y = keyboard_y
        color_key = (100,100,100)
        if highlight.get('keys') == k:
            color_key = (0, 255, 255)
        cv2.rectangle(frame, (x, y), (x+key_w, y+key_h), color_key, -1)
        cv2.putText(frame, k, (x+15, y+40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2)

    # Baris 2 offset setengah tombol
    for i, k in enumerate(keys_row2):
        x = keyboard_x + (key_w // 2) + i * (key_w + key_gap)
        y = keyboard_y + key_h + key_gap
        color_key = (100,100,100)
        if highlight.get('keys') == k:
            color_key = (0, 255, 255)
        cv2.rectangle(frame, (x, y), (x+key_w, y+key_h), color_key, -1)
        cv2.putText(frame, k, (x+15, y+40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2)

    # Baris 3 offset satu tombol penuh
    for i, k in enumerate(keys_row3):
        x = keyboard_x + key_w + i * (key_w + key_gap)
        y = keyboard_y + 2*(key_h + key_gap)
        color_key = (100,100,100)
        if highlight.get('keys') == k:
            color_key = (0, 255, 255)
        cv2.rectangle(frame, (x, y), (x+key_w, y+key_h), color_key, -1)
        cv2.putText(frame, k, (x+15, y+40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2)

    # Baris 4 spasi dan backspace
    space_x = keyboard_x + 150
    space_y = keyboard_y + 3*(key_h + key_gap)
    space_w = key_w*5 + key_gap*4
    color_space = (100,100,100)
    if highlight.get('keys') == "SPACE":
        color_space = (0, 255, 255)
    cv2.rectangle(frame, (space_x, space_y), (space_x + space_w, space_y + key_h), color_space, -1)
    cv2.putText(frame, "SPACE", (space_x + 40, space_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2)

    back_x = keyboard_x + 30
    back_y = space_y
    back_w = key_w*3 + key_gap*2
    color_back = (100,100,100)
    if highlight.get('keys') == "BACK":
        color_back = (0, 255, 255)
    cv2.rectangle(frame, (back_x, back_y), (back_x + back_w, back_y + key_h), color_back, -1)
    cv2.putText(frame, "BACK", (back_x + 20, back_y + 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2)

    # Teks hasil ketik di atas keyboard
    cv2.rectangle(frame, (keyboard_x, keyboard_y - 80), (keyboard_x + 600, keyboard_y - 20), (50,50,50), -1)
    display_text = typed_text[-60:]
    cv2.putText(frame, display_text, (keyboard_x + 10, keyboard_y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255,255,255), 2)

def check_key_press(x_finger, y_finger):
    for i, k in enumerate(keys_row1):
        x_key = keyboard_x + i * (key_w + key_gap)
        y_key = keyboard_y
        if point_in_rect(x_finger, y_finger, (x_key, y_key, x_key + key_w, y_key + key_h)):
            return k

    for i, k in enumerate(keys_row2):
        x_key = keyboard_x + (key_w // 2) + i * (key_w + key_gap)
        y_key = keyboard_y + key_h + key_gap
        if point_in_rect(x_finger, y_finger, (x_key, y_key, x_key + key_w, y_key + key_h)):
            return k

    for i, k in enumerate(keys_row3):
        x_key = keyboard_x + key_w + i * (key_w + key_gap)
        y_key = keyboard_y + 2*(key_h + key_gap)
        if point_in_rect(x_finger, y_finger, (x_key, y_key, x_key + key_w, y_key + key_h)):
            return k

    space_x = keyboard_x + 150
    space_y = keyboard_y + 3*(key_h + key_gap)
    space_w = key_w*5 + key_gap*4
    if point_in_rect(x_finger, y_finger, (space_x, space_y, space_x + space_w, space_y + key_h)):
        return "SPACE"

    back_x = keyboard_x + 30
    back_y = space_y
    back_w = key_w*3 + key_gap*2
    if point_in_rect(x_finger, y_finger, (back_x, back_y, back_x + back_w, back_y + key_h)):
        return "BACK"

    return None

def try_trigger_click(event_type):
    global last_click_left_time, last_click_right_time, last_scroll_time

    current_time = time.time()
    if event_type == "left":
        pyautogui.click(button='left')
        print("[EVENT] LEFT CLICK")

    elif event_type == "right":
        pyautogui.click(button='right')
        print("[EVENT] RIGHT CLICK")

    elif event_type == "scroll_up":
        pyautogui.scroll(100)  # Scroll up
        print("[EVENT] SCROLL UP")

    elif event_type == "scroll_down":
        pyautogui.scroll(-100)  # Scroll down
        print("[EVENT] SCROLL DOWN")

def try_trigger_key(key):
    global typed_text
    if key == "SPACE":
        typed_text += " "
        pyautogui.press('space')
    elif key == "BACK":
        typed_text = typed_text[:-1]
        pyautogui.press('backspace')
    else:
        typed_text += key
        pyautogui.press(key.lower())
    print(f"[EVENT] KEY PRESS: {key}")

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Gagal membuka kamera")
        break
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    highlight = {}

    finger_x, finger_y = None, None
    action_now = None

    if result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Pakai landmark jari telunjuk (index_finger_tip = 8)
        x_finger = int(hand_landmarks.landmark[8].x * w)
        y_finger = int(hand_landmarks.landmark[8].y * h)
        finger_x, finger_y = x_finger, y_finger

        # Draw circle finger
        cv2.circle(frame, (x_finger, y_finger), 10, (0,255,255), cv2.FILLED)

        # Check mouse areas
        if point_in_rect(x_finger, y_finger, scroll_up_area):
            highlight['scroll_up'] = True
            action_now = "scroll_up"

        elif point_in_rect(x_finger, y_finger, scroll_down_area):
            highlight['scroll_down'] = True
            action_now = "scroll_down"

        elif point_in_rect(x_finger, y_finger, click_left_area):
            highlight['left'] = True
            action_now = "left"

        elif point_in_rect(x_finger, y_finger, click_right_area):
            highlight['right'] = True
            action_now = "right"

        else:
            # Cek keyboard key
            key = check_key_press(x_finger, y_finger)
            if key:
                highlight['keys'] = key
                action_now = ("key", key)

    # Validasi debounce 1 detik
    current_time = time.time()
    if action_now is not None:
        if hold_start_time is None or hold_area != action_now:
            hold_start_time = current_time
            hold_area = action_now
            hold_key = action_now if isinstance(action_now, str) else (action_now[1] if isinstance(action_now, tuple) else None)
        else:
            if current_time - hold_start_time > DEBOUNCE_HOLD_SEC:
                # Trigger action
                if isinstance(action_now, str):
                    try_trigger_click(action_now)
                elif isinstance(action_now, tuple) and action_now[0] == "key":
                    try_trigger_key(action_now[1])
                # Reset hold timer supaya ga trigger terus
                hold_start_time = None
                hold_area = None
                hold_key = None
    else:
        hold_start_time = None
        hold_area = None
        hold_key = None

    draw_ui(frame, highlight)

    cv2.imshow("Virtual Mouse & Keyboard", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
