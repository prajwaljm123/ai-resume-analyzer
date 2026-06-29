import re

def extract_email(text):

    pattern = r'[\w\.-]+@[\w\.-]+\.\w+'

    match = re.search(pattern, text)

    return match.group() if match else None


def extract_phone(text):

    pattern = r'(\+91\s?\d{10}|\d{10})'

    match = re.search(pattern, text)

    return match.group() if match else None


def extract_name(text):

    lines = text.split("\n")

    return lines[0].strip() if lines else None