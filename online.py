import cv2
import numpy as np
from base64 import b64encode
import os
import json
import threading

# Import flask
from flask import Flask, render_template, Response

# Import firebase
import firebase_admin
from firebase_admin import credentials, db


# Import YOLOv8 dependencies
from ultralytics import YOLO


# state of positions
isfall = False
issitting = False
iswalking = False
isstanding = False
isjump = False

# flask
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


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

    #######firebase Setting#################
    # Environment Setting for using firebase
    cred = credentials.Certificate(
        "json/silvercare-84496-firebase-adminsdk-tksu6-bac3439fd8.json"
    )
    app_name = "myApp123"

    if app_name not in firebase_admin._apps:
        cur_app = firebase_admin.initialize_app(
            cred,
            {"databaseURL": "https://silvercare-84496-default-rtdb.firebaseio.com/"},
            name=app_name,
        )
    else:
        cur_app = firebase_admin.get_app(app_name)

    # Reference to the database
    ref = db.reference("/", cur_app)
    #######################################

    # Set confidence threshold and NMS threshold
    confidence_threshold = 0.5
    nms_threshold = 0.45

    # Load the YOLOv8 model
    # model = YOLO('/Users/sangwon_back/Chrome_download/IoT_Project/local_execution/pose_model.pt')
    model = YOLO("model/pose_model.pt")

    # webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 1)  # Set the frame rate to 1 FPS

    # mp4
    # cap = cv2.VideoCapture("video/falling_video.mp4")

    while True:
        global isfall

        for _ in range(5):
            cap.read()

        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection using YOLOv8
        results = model(
            frame,
            verbose=False,
            device="cpu",
            conf=confidence_threshold,
            iou=nms_threshold,
        )

        # Get the detected objects
        detections = results[0].boxes.data

        # Generate labels for the detected objects
        labels = []
        for detection in detections:
            class_id = int(detection[5])
            class_name = model.names[class_id]
            confidence = float(detection[4])
            if confidence >= confidence_threshold:
                x1, y1, x2, y2 = map(int, detection[:4])
                labels.append(f"{class_name}: {confidence:.2f}")
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"{class_name}: {confidence:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2,
                )

        ## Display the frame with detections
        # cv2.imshow('YOLOv8 Object Detection', frame)

        # Encode the frame as JPEG to be used in webpage
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        # Yield the frame in the required format
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

        # Update Firebase data in a separate thread
        if labels:
            threading.Thread(target=update_firebase, args=(ref, labels)).start()

    # # Release the capture and close windows
    # cap.release()
    # cv2.destroyAllWindows()


@app.route("/video_feed")
def video_feed():
    return Response(
        start_video_and_detect(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(debug=True)
