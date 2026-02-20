import cv2
import numpy as np
from ultralytics import YOLO
import time

# 1️⃣ Load lightweight YOLOv8 Nano detection model (Fastest for Pi)
model = YOLO("yolov8n.pt") 

cap = cv2.VideoCapture(0)

# 2️⃣ CLAHE for underwater contrast enhancement
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

while True:
    success, img = cap.read()
    if not success:
        break

    start_time = time.time()
    imgContour = img.copy()

    # --- UNDERWATER ENHANCEMENT ---
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    cl = clahe.apply(l)
    enhanced_img = cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2BGR)

    # --- YOLO DETECTION (imgsz=160 for Pi speed) ---
    results = model(enhanced_img, conf=0.4, imgsz=192)[0]

    object_counter = 1 

    for box in results.boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        # ❌ Skip person class
        if class_name.lower() == "person":
            continue

        # Bounding box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        w, h = x2 - x1, y2 - y1

        # Filter tiny boxes
        if w < 50 or h < 50:
            continue

        # --- 3️⃣ SQUARE OR RECTANGLE LOGIC ---
        # Calculate Aspect Ratio (Width / Height)
        aspect_ratio = w / float(h)
        
        # If ratio is close to 1.0, it's a Square; otherwise, it's a Rectangle
        if 0.85 < aspect_ratio < 1.15:
            shape_label = "Square"
        else:
            shape_label = "Rectangle"

        # --- DRAWING ---
        # Green box
        cv2.rectangle(imgContour, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Label object with Shape and Count
        label = f"Obj{object_counter}: {shape_label}"
        cv2.putText(imgContour, label, (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        object_counter += 1

    # Performance stats
    fps = 1 / (time.time() - start_time)
    cv2.putText(imgContour, f"FPS: {int(fps)}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow("Submarine Shape Detection", imgContour)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()