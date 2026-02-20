import cv2
import numpy as np
from ultralytics import YOLO
import time

# 1️⃣ Load lightweight YOLOv8 Nano detection model
model = YOLO("yolov8n.pt")  # Use detection model (not segmentation) for Pi speed

cap = cv2.VideoCapture(0)

# 2️⃣ CLAHE for underwater/submarine contrast enhancement
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

while True:
    success, img = cap.read()    # success captures true/false values, and img takes images inside it , this  img variable is used repeatedly to make it look like video is moving.
    if not success:
        break

    start_time = time.time()      # used to frame calculation. 
    imgContour = img.copy()       # we are creating copy of img to convert it to bgr to lab (blue gree red)(default) to (lightness Green-red  blue-yellow) color tuple.

    # --- 3️⃣ UNDERWATER CONTRAST ENHANCEMENT ---
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)    # converting image from brg to lab contrast. 
    l, a, b = cv2.split(lab)        # lab is numply array , cv2.split() takes 3d array and returns three seperate 2d arrays. 
    cl = clahe.apply(l)            # l is 2d array array of brightness vales (Hxw) , clauche.apply() enhances contrast for small  titles.
    enhanced_img = cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2BGR)  # mergting back cl , a , b and converting  image back to bgr. 

    # --- 4️⃣ YOLO DETECTION ---
    results = model(enhanced_img, conf=0.4, imgsz=192)[0]   # for raspberry pi , imgsz value should be multiple of 32, 160 or 192 is ideal. 

    object_counter = 1   # initializes counte  so we can name our objects as obj1 , obj2 etc.

    for box in results.boxes:            #results.boxes is a list of detected bounding boxes returned by YOLO for the current image
        class_id = int(box.cls[0])        #box.cls gives the class index predicted by YOLO (e.g., 0 for “person”, 1 for “bicycle”, etc.).int(box.cls[0]) converts it to a standard integer.
        class_name = model.names[class_id].lower()     #model.names[class_id] maps that index to the class name string (like "person")..lower() just converts it to lowercase so comparisons are safe (avoids "Person" vs "person" issue

        # ❌ Skip person class
        if class_name == "person":  # we shouold skip 'person' this  for  underwater detection . 
            continue

        # Bounding box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])    # box.xyxy contains bounding box coordinates in the format [x_min, y_min, x_max, y_max]. map(int, ...) converts them to integers because OpenCV drawing functions require integer coordinates.
        w, h = x2 - x1, y2 - y1      # calculating width and  height of bounding box (simply rectangular box)

        # Skip tiny boxes (noise)
        if w < 50 or h < 50:    
            continue

        # --- 5️⃣ SHAPE LOGIC (Rough for rectangles/squares/pillars/cylinders) ---
        aspect_ratio = w / float(h)   # aspect ratio = width/height.

        if 0.8 < aspect_ratio < 1.2:
            shape_label = "Square / Vertical Pillar"
        elif w > h:
            shape_label = "Horizontal Rectangle / Beam"
        else:
            shape_label = "Vertical Rectangle / Cylinder"

        # --- 6️⃣ DRAWING ---
        cv2.rectangle(imgContour, (x1, y1), (x2, y2), (0, 255, 0), 2)  # this  draws shape. imgContour: img to draw on , (x1,y1)  : top left corner , (x2,y2)  top-right corner, (0,255, 0) color of ractangle in bgr format.
        label = f"Obj{object_counter}: {shape_label}"
        cv2.putText(imgContour, label, (x1, y1 - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)  #(x1,y1-10):position the text starts. cv2.FONT_HERSHEY_SIMPLEX:font style   , 0.6: font scale , (0,255,0):bgr color. 2: thickness of textline.
        object_counter += 1

    # --- 7️⃣ PERFORMANCE METRICS ---
    fps = 1 / (time.time() - start_time)
    cv2.putText(imgContour, f"FPS: {int(fps)}", (20, 40),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # --- 8️⃣ DISPLAY SINGLE WINDOW ---
    cv2.imshow("Underwater Object Detection", imgContour)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # simply pressing q we will come out .
        break

cap.release()
cv2.destroyAllWindows()
