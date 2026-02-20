 # results = model(enhanced_img, conf=0.4, imgsz=192)[0]   # for raspberry pi , imgsz value should be multiple of 32, 160 or 192 is ideal. 

# 3️⃣ Why [0] after model(...)?
# results = model(enhanced_img, conf=0.4, imgsz=192)[0]


# model(...) always returns a list of results, even if you pass one image.
# Each element in the list corresponds to one image in a batch.
# In your case, you pass just one frame, so the list has length 1.
# [0] selects the first (and only) result object

# conf stands for confidence threshold.
# It’s a filter for the model’s predictions.

# How it works:
# YOLO predicts many boxes with probabilities for each class (how confident the model is that the object is of a certain class).

# Each box has a confidence score between 0 and 1.
# conf=0.4 means: only keep boxes with confidence ≥ 0.4. Boxes below 0.4 are ignored.

# 💡 Example:
# A box predicting a cylinder with confidence 0.35 → discarded
# A box predicting a square with confidence 0.65 → kept


# imgsz = 192     : YOLO input size (image will be resized to 192x192 before inference)
#                  Must be a multiple of 32 for YOLOv8 models
#                  Lower size → faster inference, less memory usage, may reduce detection accuracy
#                  Higher size → slower, more RAM/GPU usage, but better detection quality
#                  For Raspberry Pi 4 (8GB RAM) 192 is ideal; 160 also works but may miss small details