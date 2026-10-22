import cv2
import pytesseract
import re

# -----------------------------------
# 1. Load preprocessed certificate
# -----------------------------------

image_path = "uploads/deskewed_certificate.jpg"

image = cv2.imread(image_path)

if image is None:
    print("ERROR: Could not read image.")
    exit()

print("Preprocessed image loaded successfully!")


# -----------------------------------
# 2. Perform OCR
# -----------------------------------

text = pytesseract.image_to_string(image)

print("\n----- OCR TEXT -----")
print(text)


# -----------------------------------
# 3. Extract fields using Regex
# -----------------------------------

student_name = re.search(
    r"STUDENT NAME:\s*(.+)",
    text,
    re.IGNORECASE
)

degree = re.search(
    r"DEGREE:\s*(.+)",
    text,
    re.IGNORECASE
)

institution = re.search(
    r"INSTITUTION:\s*(.+)",
    text,
    re.IGNORECASE
)

graduation_year = re.search(
    r"GRADUATION YEAR:\s*(\d{4})",
    text,
    re.IGNORECASE
)

credential_id = re.search(
    r"CREDENTIAL ID:\s*(.+)",
    text,
    re.IGNORECASE
)


# -----------------------------------
# 4. Display structured data
# -----------------------------------

print("\n----- EXTRACTED FIELDS -----")

print(
    "Student Name:",
    student_name.group(1).strip()
    if student_name else "Not Found"
)

print(
    "Degree:",
    degree.group(1).strip()
    if degree else "Not Found"
)

print(
    "Institution:",
    institution.group(1).strip()
    if institution else "Not Found"
)

print(
    "Graduation Year:",
    graduation_year.group(1).strip()
    if graduation_year else "Not Found"
)

print(
    "Credential ID:",
    credential_id.group(1).strip()
    if credential_id else "Not Found"
)