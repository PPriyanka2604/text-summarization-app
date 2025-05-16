import re

def preprocess(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[[0-9]*\]', '', text)
    return text.strip()
