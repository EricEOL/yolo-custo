import torch
import cv2
import numpy as np

# Load YOLOv5 model directly from the Ultralytics GitHub repository
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Define the classes of interest
target_classes = ["bottle", "cup"]

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection
        results = model(frame)
        detections = results.pred[0]

        for *xyxy, conf, cls in detections:
            if model.names[int(cls)] in target_classes and conf > 0.5:
                label = model.names[int(cls)]
                x1, y1, x2, y2 = map(int, xyxy)
                color = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        out.write(frame)
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Example usage
process_video('input_video.mp4')
