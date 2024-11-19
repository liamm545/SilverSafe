import cv2
import numpy as np
from base64 import b64encode
import os
import json
import threading
import time
import servo
import audio_monitor
from ctypes import *

# Firebase imports
import firebase_admin
from firebase_admin import credentials, db

# YOLOv8 import
from ultralytics import YOLO

# Global constants
FIREBASE_CREDENTIALS_PATH = "/home/skku/SilverSafe/json/silvercare-84496-firebase-adminsdk-tksu6-bac3439fd8.json"
FIREBASE_DB_URL = "https://silvercare-84496-default-rtdb.firebaseio.com/"
YOLO_MODEL_PATH = "/home/skku/SilverSafe/model/pose_model_ncnn_model"
CONFIDENCE_THRESHOLD = 0.8
VIDEO_FPS = 60
CENTER_OFFSET_THRESHOLD = 100

# Global state
state = {
    "fall": False,
    "sitting": False,
    "walking": False,
    "standing": False,
    "jump": False,
    "loud_detected": False,
    "last_loud_detected": 0,  # Timestamp of the last loud sound
}

# ALSA error suppression setup
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass  # Suppress ALSA error messages


c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

# Load ALSA library
asound = cdll.LoadLibrary("libasound.so")
asound.snd_lib_error_set_handler(
    c_error_handler
)  # Suppress ALSA error messages globally


def monitor_audio_input():
    while True:
        if audio_monitor.get_microphone_input():
            state["loud_detected"] = True
            state["last_loud_detected"] = time.time()  # Record current time
            print("데시벨 30 이상 감지!")
        else:
            state["loud_detected"] = False
        time.sleep(0.1)


def image_to_base64(img):
    _, buffer = cv2.imencode(".jpg", img)
    return b64encode(buffer.tobytes()).decode("utf-8")


def initialize_firebase():
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    app_name = "myApp"

    if app_name not in firebase_admin._apps:
        app = firebase_admin.initialize_app(
            cred, {"databaseURL": FIREBASE_DB_URL}, name=app_name
        )
    else:
        app = firebase_admin.get_app(app_name)

    return db.reference("/", app)


def update_firebase(ref, detected_labels):
    for label in detected_labels:
        label_name, confidence = label.split(": ")
        confidence = float(confidence)

        if confidence >= CONFIDENCE_THRESHOLD:
            if not state.get(label_name, False):
                ref.update({label_name: True})
                state[label_name] = True
        else:
            if state.get(label_name, False):
                ref.update({label_name: False})
                state[label_name] = False


def process_frame(frame, model, ref):
    results = model.predict(frame)
    labels = []
    frame_height, frame_width, _ = frame.shape
    center_x = frame_width / 2
    current_time = time.time()

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cur_center = (x1 + x2) / 2
        confidence = box.conf[0]
        class_id = int(box.cls[0])
        class_name = results[0].names[class_id]
        labels.append(f"{class_name}: {confidence:.2f}")

        # Draw bounding box and label
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{class_name} ({confidence:.2f})",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        # Servo motor adjustment
        if abs(cur_center - center_x) > CENTER_OFFSET_THRESHOLD:
            print("Move servo motor")
            angle = (cur_center / frame_width) * 180
            threading.Thread(target=servo.move_motor, args=(angle,)).start()

        # Check if falling is detected within 5 seconds of loud sound
        if (
            class_name == "fall"
            and confidence >= CONFIDENCE_THRESHOLD
            and current_time - state["last_loud_detected"] <= 5
        ):
            print("Danger detected!")

    # Update Firebase with detected labels
    if labels:
        threading.Thread(target=update_firebase, args=(ref, labels)).start()

    return frame


def start_video_detection():
    ref = initialize_firebase()
    model = YOLO(YOLO_MODEL_PATH, task="pose")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, VIDEO_FPS)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = process_frame(frame, model, ref)

        # Display frame
        cv2.imshow("YOLOv8 Object Detection", frame)

        # Handle loud sound detection
        if state["loud_detected"]:
            print("데시벨 30 이상 감지!")

        # Capture frame on key press
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("c"):
            filename = f"detected_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Initialize servo motor
    servo.set_motor()

    # Start audio monitoring in a separate thread
    threading.Thread(target=monitor_audio_input, daemon=True).start()

    # Start video detection
    start_video_detection()
