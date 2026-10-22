import cv2
import pytesseract

# Preprocessed image
image_path = "uploads/deskewed_certificate.jpg"

# Read image
image = cv2.imread(image_path)

if image is None:
    print("ERROR: Could not read preprocessed image.")
    exit()

print("Preprocessed image loaded successfully!")

# OCR using Tesseract
text = pytesseract.image_to_string(image)

print("\n----- OCR OUTPUT -----")
print(text)
print("----------------------")