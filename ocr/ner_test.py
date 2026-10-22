import spacy

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Sample OCR text
text = """
STUDENT NAME: Muskah Sharma
DEGREE: Bachelor of Technology
INSTITUTION: ABC Institute of Technology
GRADUATION YEAR: 2027
CREDENTIAL ID: ABC-IT-2027-042
"""

# Process text
doc = nlp(text)

print("----- SPACY ENTITIES -----")

for entity in doc.ents:
    print(entity.text, "->", entity.label_)