import cv2
from ultralytics import YOLO
import time

model = YOLO("/home/yeong/RaspberryPI/IoT_Project/model/pose_model.pt")

video_path = "/home/yeong/RaspberryPI/IoT_Project/video/falling_video.mp4"

cap = cv2.VideoCapture(video_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    start_time = time.time()

    results = model.predict(frame, stream=True)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            confidence = box.conf[0]  # Confidence score
            class_id = int(box.cls[0])  # Class ID
            class_name = result.names[class_id]  # Get class name

            # Draw bounding box and label on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame, f"{class_name} ({confidence:.2f})", (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2
            )

    end_time = time.time()
    detection_fps = 1 / (end_time - start_time)

    cv2.imshow("Webcam Detection", frame)
    print("FPS: ", detection_fps)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()