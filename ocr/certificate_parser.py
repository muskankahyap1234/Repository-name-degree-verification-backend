import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_certificate_data(text):

    # Process text with spaCy
    doc = nlp(text)

    # -------------------------
    # Extract using Regex
    # -------------------------

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

    # -------------------------
    # Create structured data
    # -------------------------

    certificate_data = {
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

    return certificate_data


# -------------------------
# Test
# -------------------------

text = """
STUDENT NAME: Muskah Sharma
DEGREE: Bachelor of Technology
INSTITUTION: ABC Institute of Technology
GRADUATION YEAR: 2027
CREDENTIAL ID: ABC-IT-2027-042
"""

data = extract_certificate_data(text)

print("----- CERTIFICATE DATA -----")

for key, value in data.items():
    print(f"{key}: {value}")