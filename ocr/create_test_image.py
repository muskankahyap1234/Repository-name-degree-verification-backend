import cv2
import numpy as np

# White background
image = np.ones((800, 1200, 3), dtype=np.uint8) * 255

# Text
texts = [
    "SAMPLE OCR TEST DOCUMENT",
    "STUDENT NAME: Muskan Sharma",
    "DEGREE: Bachelor of Technology",
    "INSTITUTION: ABC Institute of Technology",
    "GRADUATION YEAR: 2027",
    "CREDENTIAL ID: ABC-IT-2027-042",
    "FOR OCR TESTING ONLY"
]

y = 100

for text in texts:
    cv2.putText(
        image,
        text,
        (80, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 0, 0),
        2
    )
    y += 100

# Save image
cv2.imwrite("uploads/certificate.jpg", image)

print("Test image created successfully!")