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
CENTER_OFFSET_THRESHOLD = 50  # Threshold for detecting offset from center

# Global state
state = {
    # "fall": False,
    # "sitting": False,
    # "walking": False,
    # "standing": False,
    # "jump": False,
    "is_sleep" : False,
    "last_sitting_time" : 0,
    "last_warning_time" : 0,
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

# JACK error suppression setup
JACK_ERROR_HANDLER_FUNC = CFUNCTYPE(None)


def py_jack_error_handler():
    pass  # Suppress JACK error messages


jack_c_error_handler = JACK_ERROR_HANDLER_FUNC(py_jack_error_handler)

# Load JACK library
try:
    jack = cdll.LoadLibrary("libjack.so.0")
    jack.jack_set_error_function(jack_c_error_handler)
except OSError:
    print("JACK library not found. Continuing without JACK error suppression.")


def monitor_audio_input():
    while True:
        if audio_monitor.get_microphone_input():
            state["loud_detected"] = True
            state["last_loud_detected"] = time.time()  # Record current time
            print("Sound level above 30 dB detected!")
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
        current_time = time.time()

        
        if confidence >= CONFIDENCE_THRESHOLD:
            if not state.get(label_name, False):
                ref.update({label_name: True})
                if(label_name == "sitting"):
                    state["last_sitting_time"] = current_time
                elif(label_name == "fall"):
                    if(state["is_sleep"]): continue # stop detecting when sleeping
                    if(current_time - state["last_warning_time"] < 5) : continue # stop detecting for 5 sec after warning detected
                    print("last_sitting_time : ", state["last_sitting_time"])
                    print("current time: ", current_time)
                    if(current_time - state["last_sitting_time"] <= 3): # sitting detected within 3 sec
                        print("sleep")
                        state["is_sleep"] = True
                    else:
                        if((state["loud_detected"] == True) and (current_time - state["last_loud_detected"] <= 5)): # loud sound detected within 5 sec
                            print("Warning: loud sound O")
                            ref.update({"danger" : True})
                            state["last_warning_time"] = time.time()
                            ref.update({"danger" : False})
                        else:
                            print("Caution: lound sound X")
                elif(label_name == "standing" and state["is_sleep"] == True):
                        state["is_sleep"] = False    
                #state[label_name] = True
        else:
            if state.get(label_name, False):
                ref.update({label_name: False})
                #state[label_name] = False


def process_frame(frame, model, ref):
    results = model.predict(frame)
    labels = []
    frame_height, frame_width, _ = frame.shape
    center_x = frame_width / 2
    #current_time = time.time()

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

        # Adjust servo motor if the person is not centered
        offset = cur_center - center_x
        if abs(offset) > CENTER_OFFSET_THRESHOLD and labels:
            current_angle = servo.get_current_angle()
            adjustment = offset / center_x * 30  # Adjust angle proportionally
            target_angle = current_angle + adjustment
            target_angle = max(
                servo.MIN_ANGLE, min(servo.MAX_ANGLE, target_angle)
            )  # Clamp to valid range
            # print(
            #     f"Person detected off-center. Adjusting servo: {current_angle}° -> {target_angle}°"
            # )
            threading.Thread(target=servo.move_motor, args=(target_angle,)).start()

        # # Check if falling is detected within 5 seconds of loud sound
        # if (
        #     class_name == "fall"
        #     and confidence >= CONFIDENCE_THRESHOLD
        #     and current_time - state["last_loud_detected"] <= 5
        # ):
        #     print("Danger detected!")

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
        # if state["loud_detected"]:
        #     print("Sound level above 30 dB detected!")

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
    # Initialize servo motor at 90 degrees
    # servo.set_servo_angle(90)

    # Start audio monitoring in a separate thread
    threading.Thread(target=monitor_audio_input, daemon=True).start()

    # Start video detection
    start_video_detection()
