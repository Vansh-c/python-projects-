import cv2
import numpy as np
import time

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

cap = cv2.VideoCapture(1) # Change to 1 if using external cam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

# Memory for Stability
confidence_score = 0
MEMORY_CAP = 15
last_gate_rect = None # Stores [x, y, w, h]
smooth_error_x = 0

while True:
    ret, frame = cap.read()
    if not ret: break

    start_time = time.perf_counter()
    h, w, _ = frame.shape
    imgContour = frame.copy()

    # 1. Color Masking (Broad for red/orange rods)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 100, 60])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([165, 100, 60])
    upper_red2 = np.array([180, 255, 255])

    mask = cv2.bitwise_or(cv2.inRange(hsv, lower_red1, upper_red1), 
                          cv2.inRange(hsv, lower_red2, upper_red2))

    # Clean noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 2. Filtering for Vertical Rods
    rods = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 400: continue

        bx, by, bw, bh = cv2.boundingRect(cnt)
        aspect_ratio = bw / float(bh)

        # Only accept thin, vertical objects
        if aspect_ratio < 0.5:
            rods.append({'x': bx, 'y': by, 'w': bw, 'h': bh, 'cx': bx + bw//2})

    # Sort by height to find the two main bars
    rods = sorted(rods, key=lambda r: r['h'], reverse=True)[:2]

    valid_gate = False
    if len(rods) == 2:
        r1, r2 = rods[0], rods[1]
        
        # Parallel Logic: Similar height and Y-level
        height_diff = min(r1['h'], r2['h']) / float(max(r1['h'], r2['h']))
        y_alignment = abs(r1['y'] - r2['y'])
        dist = abs(r1['cx'] - r2['cx'])

        if height_diff > 0.6 and y_alignment < 60 and (dist > 50):
            valid_gate = True
            
            # 3. Calculate the CLEAN Rectangle between the bars
            left_x = min(r1['x'], r2['x'])
            right_x = max(r1['x'] + r1['w'], r2['x'] + r2['w'])
            top_y = min(r1['y'], r2['y'])
            bottom_y = max(r1['y'] + r1['h'], r2['y'] + r2['h'])
            
            last_gate_rect = (left_x, top_y, right_x - left_x, bottom_y - top_y)
            gate_center = (r1['cx'] + r2['cx']) // 2
            smooth_error_x = int(0.8 * smooth_error_x + 0.2 * (gate_center - w//2))

    # --- Persistence Logic ---
    if valid_gate:
        confidence_score = min(MEMORY_CAP, confidence_score + 3)
    else:
        confidence_score = max(0, confidence_score - 1)

    # 4. Final Render (The "Locked" State)
    if confidence_score > 4 and last_gate_rect is not None:
        gx, gy, gw, gh = last_gate_rect
        overlay = frame.copy()
        
        # FILL ONLY THE RECTANGLE
        cv2.rectangle(overlay, (gx, gy), (gx + gw, gy + gh), (0, 255, 120), -1)
        
        alpha = clamp(confidence_score / float(MEMORY_CAP), 0.1, 0.4)
        imgContour = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

        cv2.putText(imgContour, f"LOCKED: {smooth_error_x}px", (w//2 - 100, h - 30), 
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 120), 2)
    else:
        cv2.putText(imgContour, "SCANNING...", (20, h - 30), 1, 0.7, (0,0,255), 2)

    # Performance
    fps = 1 / (time.perf_counter() - start_time)
    cv2.putText(imgContour, f"FPS: {int(fps)}", (10, 30), 1, 0.6, (255,255,255), 1)

    cv2.imshow("SUBMARINE NAV", imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()