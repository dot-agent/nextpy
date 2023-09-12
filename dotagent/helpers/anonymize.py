import re
import spacy

class PIIScrubber:
    """
    Class for scrubbing personally identifiable information (PII) from text.
    """
    PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
        'ssn': r'\d{3}-?\d{2}-?\d{4}',
        'credit_card': r'\d{4}-?\d{4}-?\d{4}-?\d{4}',
        'phone_number': r'\b(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
        'ip': r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
        'date_of_birth': r'\b(0[1-9]|1[0-2])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d\b',
        'vehicle_identification_number': r'\b([A-HJ-NPR-Z0-9]{3})([A-HJ-NPR-Z0-9]{5})(\d{2})([A-HJ-NPR-Z0-9]{8})\b',
    }

    def __init__(self, verbose=False):
        """
        Initialize the PIIScrubber with given verbosity.

        Args:
            verbose (bool): If True, print out internal states. Default is False.
        """
        self.verbose = verbose
        self.nlp = spacy.load('en_core_web_sm')

    def scrub(self, text):
        """
        Detect and log PII in the given text based on regex patterns and SpaCy NER.
    
        Args:
            text (str): The input text to scrub.

        Returns:
            dict: A dictionary with the start and end indices of the detected PII as keys and the corresponding replacements as values.
        """
        replacements = {}
        for label, pattern in self.PATTERNS.items():
            for match in re.finditer(pattern, text):
                replacements[match.span()] = f"[REDACTED {label.upper()}]"
                if self.verbose:
                    print(f"Potential {label} detected: {match.group()}")

        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in ['PERSON', 'ORG']:
                replacements[ent.start_char, ent.end_char] = "[REDACTED NAME]"
                if self.verbose:
                    print(f"Potential {ent.label_} entity detected: {ent.text}")

        return replacements

    @staticmethod
    def anonymize_text(text, replacements):
        """
        Anonymize PII in the given text based on the provided replacements.
    
        Args:
            text (str): The input text to anonymize.
            replacements (dict): A dictionary with the start and end indices of the PII to replace as keys and the corresponding replacements as values.

        Returns:
            str: The anonymized text.
        """
        replacements = sorted(replacements.items(), key=lambda x: x[0][0], reverse=True)
        for (start, end), replacement in replacements:
            text = text[:start] + replacement + text[end:]

        return text

    def run(self, text):
        """
        Detect, log, and anonymize PII in the given text.
    
        Args:
            text (str): The input text to scrub.

        Returns:
            str: The anonymized text.
        """
        if not isinstance(text, str):
            raise TypeError('Text must be a string')

        try:
            replacements = self.scrub(text)
            anonymized_text = self.anonymize_text(text, replacements)
            if text != anonymized_text and self.verbose:
                print(f'Original: {text}\nAnonymized: {anonymized_text}')

        except Exception as e:
            print(f"Error processing text: {e}")
            raise e

        return anonymized_text
