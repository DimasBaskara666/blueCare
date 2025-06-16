import re
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class NLPEngine:
    def __init__(self):
        # Initialize Sastrawi components
        self.stemmer = StemmerFactory().create_stemmer()
        self.stopword_remover = StopWordRemoverFactory().create_stop_word_remover()
        
        # Common medical terms in Indonesian (to be expanded)
        self.medical_terms = {
            "demam": "demam",
            "sakit kepala": "sakit_kepala",
            "batuk": "batuk",
            "pilek": "pilek",
            "mual": "mual",
            "muntah": "muntah",
            "diare": "diare",
            "sakit perut": "sakit_perut",
            "sesak nafas": "sesak_nafas",
            "nyeri": "nyeri",
            "pusing": "pusing",
            "lemas": "lemas",
            "meriang": "meriang",
            "gatal": "gatal",
            "ruam": "ruam",
        }

    def clean_text(self, text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def tokenize(self, text):
        """Tokenize text into words"""
        return nltk.word_tokenize(text)

    def remove_stopwords(self, tokens):
        """Remove Indonesian stopwords"""
        text = ' '.join(tokens)
        return self.stopword_remover.remove(text).split()

    def stem_words(self, tokens):
        """Stem words using Sastrawi"""
        text = ' '.join(tokens)
        return self.stemmer.stem(text).split()

    def extract_medical_terms(self, tokens):
        """Extract and normalize medical terms"""
        extracted_terms = []
        text = ' '.join(tokens)
        
        # Check for multi-word terms first
        for term, normalized in self.medical_terms.items():
            if term in text:
                extracted_terms.append(normalized)
                text = text.replace(term, '')
        
        # Add remaining single words
        remaining_tokens = text.split()
        extracted_terms.extend(remaining_tokens)
        
        return list(set(extracted_terms))  # Remove duplicates

    def process(self, text):
        """Process text through the complete NLP pipeline"""
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(cleaned_text)
        
        # Remove stopwords
        tokens = self.remove_stopwords(tokens)
        
        # Stem words
        tokens = self.stem_words(tokens)
        
        # Extract medical terms
        medical_terms = self.extract_medical_terms(tokens)
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'tokens': tokens,
            'medical_terms': medical_terms
        }

# Global NLP engine instance
_nlp_engine = None

def initialize_nlp():
    """Initialize the global NLP engine"""
    global _nlp_engine
    if _nlp_engine is None:
        _nlp_engine = NLPEngine()

def process_symptoms(text):
    """Process symptoms text using the global NLP engine"""
    if _nlp_engine is None:
        initialize_nlp()
    return _nlp_engine.process(text) 