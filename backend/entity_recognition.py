import spacy
import re

class EntityRecognizer:
    def __init__(self):
        # Load the spaCy model for named entity recognition
        self.nlp = spacy.load('en_core_web_sm')

    def extract_entities(self, text):
        # Extract named entities using spaCy
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    def extract_emails(self, text):
        # Extract emails using regex
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        return emails

    def extract_phone_numbers(self, text):
        # Extract phone numbers using regex
        phone_pattern = r'\+?\d?[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}'
        phone_numbers = re.findall(phone_pattern, text)
        return phone_numbers
