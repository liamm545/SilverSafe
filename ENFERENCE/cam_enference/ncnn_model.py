import cv2
from ultralytics import YOLO
import time

ncnn_model = YOLO("/home/skku_3/Rasp/IoT_Project/model/pose_model_ncnn_model", task="pose")

cap = cv2.VideoCapture(0)

fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    start_time = time.time()

    results = ncnn_model.predict(frame)
    boxes = results[0].boxes

    # Draw bounding boxes
    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = box.conf[0]
        class_id = int(box.cls[0])
        class_name = results[0].names[class_id]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame, f"{class_name} ({confidence:.2f})", (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
        )

    cv2.imshow("HIHI", frame)

    end_time = time.time()
    detection_fps = 1 / (end_time - start_time)

    print("FPS: ", detection_fps)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()