import cv2
import pytesseract
import re
import spacy


# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def process_certificate(image_path):

    # --------------------------------
    # 1. Read uploaded certificate
    # --------------------------------

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Could not read certificate image.")

    # --------------------------------
    # 2. Grayscale
    # --------------------------------

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # --------------------------------
    # 3. Adaptive Gaussian Threshold
    # --------------------------------

    threshold = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # --------------------------------
    # 4. Bilateral Filtering
    # --------------------------------

    filtered = cv2.bilateralFilter(
        threshold,
        9,
        75,
        75
    )

    # --------------------------------
    # 5. Deskew using Hough Transform
    # --------------------------------

    edges = cv2.Canny(
        filtered,
        50,
        150,
        apertureSize=3
    )

    lines = cv2.HoughLines(
        edges,
        1,
        3.14159 / 180,
        150
    )

    angle = 0

    if lines is not None:

        angles = []

        for line in lines:

            rho, theta = line[0]

            degree = theta * 180 / 3.14159

            if degree > 90:
                degree -= 180

            if -45 < degree < 45:
                angles.append(degree)

        if angles:
            angles.sort()
            angle = angles[len(angles) // 2]

    # Rotate image
    height, width = filtered.shape[:2]

    center = (width // 2, height // 2)

    rotation_matrix = cv2.getRotationMatrix2D(
        center,
        angle,
        1.0
    )

    deskewed = cv2.warpAffine(
        filtered,
        rotation_matrix,
        (width, height),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )

    # --------------------------------
    # 6. Tesseract OCR
    # --------------------------------

    text = pytesseract.image_to_string(deskewed)

    # --------------------------------
    # 7. spaCy processing
    # --------------------------------

    doc = nlp(text)

    # --------------------------------
    # 8. Regex extraction
    # --------------------------------

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

    # --------------------------------
    # 9. Structured result
    # --------------------------------

    certificate_data = {
        "student_name": (
            student_name.group(1).strip()
            if student_name else None
        ),

        "degree": (
            degree.group(1).strip()
            if degree else None
        ),

        "institution": (
            institution.group(1).strip()
            if institution else None
        ),

        "graduation_year": (
            graduation_year.group(1).strip()
            if graduation_year else None
        ),

        "credential_id": (
            credential_id.group(1).strip()
            if credential_id else None
        )
    }

    return{
        "ocr_text": text,
        "certificate_data": certificate_data
    }