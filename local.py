import cv2
import numpy as np
from base64 import b64encode
import os
import json
import threading
import time
import servo
import audio_monitor

# Import firebase
import firebase_admin
from firebase_admin import credentials, db

# Import YOLOv8 dependencies
from ultralytics import YOLO

# State variable for loud sound detection
# State of positions
isfall = False
issitting = False
iswalking = False
isstanding = False
isjump = False
loud_detected = False

# Function to monitor microphone input in a separate thread
def monitor_audio_input():
    global loud_detected
    while True:
        if audio_monitor.get_microphone_input():
            loud_detected = True
            print("데시벨 30 이상 감지!")
        else:
            loud_detected = False
        time.sleep(0.1)  # 너무 빠른 감지 방지를 위해 짧은 대기 시간 추가

# Function to convert OpenCV image to base64 string
def image_to_base64(img):
    _, buffer = cv2.imencode(".jpg", img)
    img_bytes = buffer.tobytes()
    img_b64 = b64encode(img_bytes).decode("utf-8")
    return img_b64


# Firebase update function
def update_firebase(ref, labels):
    global isfall, issitting, iswalking, isstanding, isjump

    for label in labels:
        label_name = label.split(": ")[0]
        pos = label.split(": ")[1]
        if float(pos) > 0.8:
            if label_name == "fall":
                ref.update({"fall": True})
                isfall = True
            elif label_name == "jump":
                ref.update({"jump": True})
                isjump = True
            elif label_name == "sitting":
                ref.update({"sitting": True})
                issitting = True
            elif label_name == "standing":
                ref.update({"standing": True})
                isstanding = True
            elif label_name == "walking":
                ref.update({"walking": True})
                iswalking = True
        else:
            if isfall:
                ref.update({"fall": False})
                isfall = False
            if isjump:
                ref.update({"jump": False})
                isjump = False
            if isstanding:
                ref.update({"standing": False})
                isstanding = False
            if issitting:
                ref.update({"sitting": False})
                issitting = False
            if iswalking:
                ref.update({"walking": False})
                iswalking = False


# Function to start the video stream and perform object detection
def start_video_and_detect():
    ####### Firebase Setting #################
    cred = credentials.Certificate(
        "/home/skku/SilverSafe/json/silvercare-84496-firebase-adminsdk-tksu6-bac3439fd8.json"
    )

    app_name = "myApp"

    if app_name not in firebase_admin._apps:
        cur_app = firebase_admin.initialize_app(
            cred,
            {"databaseURL": "https://silvercare-84496-default-rtdb.firebaseio.com/"},
            name=app_name,
        )
    else:
        cur_app = firebase_admin.get_app(app_name)

    ref = db.reference("/", cur_app)
    #######################################

    confidence_threshold = 0.5
    nms_threshold = 0.45

    ncnn_model = YOLO(
        "/home/skku/SilverSafe/model/pose_model_ncnn_model", task="pose"
    )

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 60)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while True:
        global isfall, loud_detected

        ret, frame = cap.read()
        if not ret:
            break

        cur_height, cur_width, _ = frame.shape
        center_x = cur_width / 2

        results = ncnn_model.predict(frame)
        boxes = results[0].boxes

        labels = []
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cur_center = (x1 + x2) / 2
            confidence = box.conf[0]
            class_id = int(box.cls[0])
            class_name = results[0].names[class_id]
            labels.append(f"{class_name}: {confidence:.2f}")
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

            if abs(cur_center - center_x) > 100:
                print("Move")
                tmp_dir = (cur_center / cur_width) * 180
                threading.Thread(
                    target=servo.move_motor, args=(tmp_dir,)
                ).start()

        cv2.imshow("YOLOv8 Object Detection", frame)

        # Check if loud sound was detected
        if loud_detected:
            print("데시벨 30 이상 감지!")

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        if labels:
            threading.Thread(target=update_firebase, args=(ref, labels)).start()

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("c"):
            filename = "_".join(labels) + ".jpg"
            filename = filename.replace(":", "_")
            filename = filename.replace(" ", "_")
            cv2.imwrite(filename, frame)

    cap.release()
    cv2.destroyAllWindows()


# Main function
def main():
    servo.set_motor()

    # Start audio monitoring thread
    audio_thread = threading.Thread(target=monitor_audio_input, daemon=True)
    audio_thread.start()

    # Start video detection
    start_video_and_detect()


if __name__ == "__main__":
    main()
