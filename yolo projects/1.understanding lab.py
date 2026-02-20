# Q:    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB). 

# 1️⃣ How images are stored in a computer

# Think of your image as a grid of pixels:
# Suppose your image is 5×5 pixels (tiny for example).
# Each pixel has a color. In BGR, that color is 3 numbers: [B, G, R].
# So the image is stored like a 3D array:

# Height × Width × Channels
# Height = number of rows (pixels vertically)
# Width = number of columns (pixels horizontally)
# Channels = 3 (B, G, R)

# Example for a 5×5 BGR image:
# img.shape -> (5, 5, 3)




# 1️⃣ What is LAB Color Space?

# LAB is a color space designed to separate lightness from color, which is very useful for vision tasks where lighting conditions can change (like underwater).

# L = Lightness (0 → 0% black, 100 → 100% white)
# A = Green–Red axis (negative → green, positive → red)
# B = Blue–Yellow axis (negative → blue, positive → yellow)

# 💡 Why use LAB instead of RGB?
# RGB mixes color and brightness, so if lighting changes (sun, underwater, shadows), your object detection might fail.
# LAB isolates lightness in L, so you can enhance contrast without messing up the colors in A and B.



# 2️⃣ How OpenCV handles LAB
# In OpenCV:
# lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)


# img → your original image in BGR format (OpenCV default).
# lab → a 3D numpy array with shape (height, width, 3)
# Think of lab as three layers stacked together:

# lab[:,:,0] = L channel
# lab[:,:,1] = A channel
# lab[:,:,2] = B channel

# For one pixel, you could imagine it like:

# lab[100, 200]  # pixel at row 100, col 200
# Might output: [120, 135, 90]
# L = 120, A = 135, B = 90


# understanding though above is written this  is for more clarity . 
# Before split:

# You have an image: img.shape = (height, width, 3)
# Example: (5,5,3)

# Each pixel looks like: [L, A, B] (after cv2.cvtColor
# Think of it as a 3D array: the first two dimensions are spatial (height & width), the last dimension is color channels (3 numbers per pixel).
# Pixel at (2,3) -> lab[2,3] = [L_value, A_value, B_value]

# After cv2.split(lab):
# l, a, b = cv2.split(lab)
# l.shape = (5,5) → 2D array of lightness values