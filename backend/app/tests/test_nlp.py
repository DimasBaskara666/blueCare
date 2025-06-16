import unittest
from unittest.mock import patch, MagicMock
import nltk
from app.nlp.engine import NLPEngine

class TestNLPEngine(unittest.TestCase):
    def setUp(self):
        self.nlp_engine = NLPEngine()
        self.sample_text = "Saya mengalami demam tinggi dan batuk kering sejak 3 hari yang lalu"

    def test_clean_text(self):
        """Test text cleaning functionality"""
        # Test with normal text
        cleaned = self.nlp_engine.clean_text(self.sample_text)
        self.assertIsInstance(cleaned, str)
        self.assertNotIn("  ", cleaned)  # No double spaces
        
        # Test with text containing special characters
        text_with_special = "Saya mengalami demam! @#$%^&*()"
        cleaned = self.nlp_engine.clean_text(text_with_special)
        self.assertNotIn("@#$%^&*()", cleaned)
        
        # Test with text containing numbers
        text_with_numbers = "Suhu tubuh 38.5 derajat"
        cleaned = self.nlp_engine.clean_text(text_with_numbers)
        self.assertIn("38.5", cleaned)  # Numbers should be preserved

    def test_tokenize(self):
        """Test text tokenization"""
        tokens = self.nlp_engine.tokenize(self.sample_text)
        
        self.assertIsInstance(tokens, list)
        self.assertTrue(all(isinstance(token, str) for token in tokens))
        self.assertIn("demam", tokens)
        self.assertIn("batuk", tokens)

    def test_remove_stopwords(self):
        """Test stopword removal"""
        tokens = ["saya", "mengalami", "demam", "dan", "batuk"]
        filtered = self.nlp_engine.remove_stopwords(tokens)
        
        self.assertIsInstance(filtered, list)
        self.assertNotIn("saya", filtered)  # Should be removed
        self.assertNotIn("dan", filtered)   # Should be removed
        self.assertIn("demam", filtered)    # Should be kept
        self.assertIn("batuk", filtered)    # Should be kept

    def test_stem_words(self):
        """Test word stemming"""
        tokens = ["mengalami", "demam", "batuk"]
        stemmed = self.nlp_engine.stem_words(tokens)
        
        self.assertIsInstance(stemmed, list)
        self.assertTrue(all(isinstance(token, str) for token in stemmed))
        self.assertIn("alami", stemmed)  # "mengalami" should be stemmed to "alami"
        self.assertIn("demam", stemmed)  # "demam" should remain unchanged
        self.assertIn("batuk", stemmed)  # "batuk" should remain unchanged

    def test_extract_medical_terms(self):
        """Test medical term extraction"""
        tokens = ["demam", "batuk", "sakit", "kepala", "mual"]
        medical_terms = self.nlp_engine.extract_medical_terms(tokens)
        
        self.assertIsInstance(medical_terms, list)
        self.assertIn("demam", medical_terms)
        self.assertIn("batuk", medical_terms)
        self.assertIn("sakit_kepala", medical_terms)
        self.assertIn("mual", medical_terms)

    def test_process_text(self):
        """Test complete text processing pipeline"""
        result = self.nlp_engine.process_text(self.sample_text)
        
        self.assertIsInstance(result, dict)
        self.assertIn("tokens", result)
        self.assertIn("medical_terms", result)
        
        # Check if medical terms are extracted
        self.assertIn("demam", result["medical_terms"])
        self.assertIn("batuk", result["medical_terms"])
        
        # Check if tokens are cleaned and stemmed
        self.assertTrue(all(isinstance(token, str) for token in result["tokens"]))
        self.assertNotIn("saya", result["tokens"])  # Stopword should be removed

    def test_normalize_medical_terms(self):
        """Test medical term normalization"""
        # Test with common variations
        variations = [
            "demam tinggi",
            "demam",
            "panas",
            "suhu tubuh tinggi"
        ]
        
        for term in variations:
            normalized = self.nlp_engine.normalize_medical_term(term)
            self.assertEqual(normalized, "demam")
        
        # Test with non-medical terms
        non_medical = "makan"
        normalized = self.nlp_engine.normalize_medical_term(non_medical)
        self.assertEqual(normalized, non_medical)  # Should remain unchanged

    def test_handle_empty_input(self):
        """Test handling of empty input"""
        # Test with empty string
        result = self.nlp_engine.process_text("")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result["tokens"]), 0)
        self.assertEqual(len(result["medical_terms"]), 0)
        
        # Test with whitespace only
        result = self.nlp_engine.process_text("   ")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result["tokens"]), 0)
        self.assertEqual(len(result["medical_terms"]), 0)

    def test_handle_special_characters(self):
        """Test handling of special characters"""
        text = "Suhu tubuh: 38.5°C, tekanan darah: 120/80 mmHg"
        result = self.nlp_engine.process_text(text)
        
        self.assertIsInstance(result, dict)
        self.assertIn("suhu", result["tokens"])
        self.assertIn("tekanan_darah", result["medical_terms"])

if __name__ == '__main__':
    unittest.main() 