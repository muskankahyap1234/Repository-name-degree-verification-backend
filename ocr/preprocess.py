
import cv2
import numpy as np
import math

image_path = "uploads/certificate.jpg"

# Read image
image = cv2.imread(image_path)

if image is None:
    print("ERROR: Could not read image.")
    exit()

print("Image loaded successfully!")

# Step 1: Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imwrite("uploads/gray_certificate.jpg", gray)

print("Grayscale conversion completed!")

# Step 2: Adaptive Gaussian Thresholding
threshold = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)

cv2.imwrite("uploads/threshold_certificate.jpg", threshold)

print("Adaptive Gaussian thresholding completed!")

# Step 3: Bilateral Noise Filtering
filtered = cv2.bilateralFilter(
    threshold,
    9,
    75,
    75
)

cv2.imwrite("uploads/filtered_certificate.jpg", filtered)

print("Bilateral noise filtering completed!")

# Step 4: Deskew using Hough Line Transform

# Detect edges
edges = cv2.Canny(filtered, 50, 150, apertureSize=3)

# Detect lines
lines = cv2.HoughLines(edges, 1, np.pi / 180, 150)

angle = 0

if lines is not None:
    angles = []

    for line in lines:
        rho, theta = line[0]

        # Convert angle from radians to degrees
        degree = theta * 180 / np.pi

        # Convert to text-line angle
        if degree > 90:
            degree -= 180

        if -45 < degree < 45:
            angles.append(degree)

    if angles:
        angle = np.median(angles)

print("Detected angle:", angle)

# Rotate image to correct skew
(h, w) = filtered.shape[:2]
center = (w // 2, h // 2)

rotation_matrix = cv2.getRotationMatrix2D(
    center,
    angle,
    1.0
)

deskewed = cv2.warpAffine(
    filtered,
    rotation_matrix,
    (w, h),
    flags=cv2.INTER_CUBIC,
    borderMode=cv2.BORDER_REPLICATE
)

cv2.imwrite("uploads/deskewed_certificate.jpg", deskewed)

print("Deskewing completed!")