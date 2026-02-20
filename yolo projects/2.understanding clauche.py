#Q:  cl = clahe.apply(l)

# 1️⃣ What CLAHE is:

# CLAHE = Contrast Limited Adaptive Histogram Equalization
# It’s a smart contrast enhancer.
# Regular histogram equalization brightens the whole image globally.
# CLAHE works locally, enhancing contrast in small tiles.
# “ClipLimit” prevents over-amplifying noise.


# 2️⃣ Why we apply it to l only:

# l = lightness channel of LAB (brightness information).
# a and b = color information (green-red, blue-yellow).
# Underwater, colors fade but brightness is still useful.
# Enhancing only L brightens/sharpens objects without messing colors.


# 3️⃣ What happens with this line:
# cl = clahe.apply(l)


# l is a 2D array of brightness values (H × W).
# clahe.apply(l) enhances local contrast for every small tile (e.g., 8×8 pixels if tileGridSize=(8,8))
# The output cl is also a 2D array, now with enhanced brightness.
# Areas that were dark become clearer, areas that were bright remain bright (no clipping too high)


# 4️⃣ Then we merge it back:
# enhanced_img = cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2BGR)


# Replace the original L channel with the enhanced one.
# Merge a and b (colors) back.
# Convert to BGR → now you have a visually clearer image, perfect for YOLO detection.
# 💡 Intuition: CLAHE makes faint underwater objects “pop” without distorting their color, which helps your YOLO model detect them better.
