import cv2
import pytesseract
import re
import spacy


# -------------------------
# Load spaCy model
# -------------------------
nlp = spacy.load("en_core_web_sm")


# -------------------------
# Certificate parser
# -------------------------
def extract_certificate_data(text):

    doc = nlp(text)

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

    return {
        "student_name": student_name.group(1).strip()
        if student_name else None,

        "degree": degree.group(1).strip()
        if degree else None,

        "institution": institution.group(1).strip()
        if institution else None,

        "graduation_year": graduation_year.group(1).strip()
        if graduation_year else None,

        "credential_id": credential_id.group(1).strip()
        if credential_id else None
    }


# -------------------------
# 1. Load processed image
# -------------------------
image_path = "uploads/deskewed_certificate.jpg"

image = cv2.imread(image_path)

if image is None:
    print("ERROR: Could not read image.")
    exit()

print("Image loaded successfully!")


# -------------------------
# 2. OCR
# -------------------------
text = pytesseract.image_to_string(image)

print("\n----- OCR TEXT -----")
print(text)


# -------------------------
# 3. Extract certificate data
# -------------------------
certificate_data = extract_certificate_data(text)


# -------------------------
# 4. Display final result
# -------------------------
print("\n----- FINAL CERTIFICATE DATA -----")

for key, value in certificate_data.items():
    print(f"{key}: {value}")