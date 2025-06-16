import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from datetime import datetime

from app.core.predictor import DiseasePredictor, DummyModel
from app.core.chatbot import HealthAssistant
from app.utils.helpers import (
    format_prediction,
    handle_numpy_types,
    create_error_response,
    create_success_response
)

class TestDiseasePredictor(unittest.TestCase):
    def setUp(self):
        self.predictor = DiseasePredictor()
        self.sample_symptoms = ["demam", "batuk", "sakit kepala"]

    def test_dummy_model_prediction(self):
        model = DummyModel()
        prediction = model.predict(self.sample_symptoms)
        
        # Check if prediction is a dictionary
        self.assertIsInstance(prediction, dict)
        
        # Check if all values are between 0 and 1
        for prob in prediction.values():
            self.assertTrue(0 <= prob <= 1)
        
        # Check if probabilities sum to approximately 1
        total_prob = sum(prediction.values())
        self.assertAlmostEqual(total_prob, 1.0, places=2)

    def test_format_prediction(self):
        prediction = {
            "Flu": 0.6,
            "Common Cold": 0.3,
            "COVID-19": 0.1
        }
        
        formatted = format_prediction(prediction, top_n=2)
        
        # Check if we get the correct number of results
        self.assertEqual(len(formatted), 2)
        
        # Check if results are sorted by probability
        self.assertEqual(formatted[0]["disease"], "Flu")
        self.assertEqual(formatted[0]["probability"], 0.6)
        self.assertEqual(formatted[0]["percentage"], "60.0%")

class TestHealthAssistant(unittest.TestCase):
    def setUp(self):
        self.chatbot = HealthAssistant()

    def test_general_questions(self):
        # Test greeting
        response = self.chatbot.get_response("halo")
        self.assertIn("Halo!", response["response"])
        
        # Test thank you
        response = self.chatbot.get_response("terima kasih")
        self.assertIn("Sama-sama", response["response"])
        
        # Test COVID-19 question
        response = self.chatbot.get_response("apa gejala covid")
        self.assertIn("COVID-19", response["response"])

    def test_symptom_questions(self):
        context = {"medical_terms": ["demam", "batuk"]}
        response = self.chatbot.get_response("saya demam", context)
        
        # Check if response contains follow-up questions
        self.assertIn("Berapa suhu tubuh Anda?", response["response"])
        self.assertIn("Apakah batuk berdahak?", response["response"])

    def test_health_advice(self):
        context = {"medical_terms": ["demam"]}
        response = self.chatbot.get_response("saya demam", context)
        
        # Check if response contains health advice
        self.assertIn("Untuk demam:", response["response"])
        self.assertIn("Istirahat yang cukup", response["response"])

class TestHelpers(unittest.TestCase):
    def test_handle_numpy_types(self):
        # Test numpy integer
        self.assertEqual(handle_numpy_types(np.int64(42)), 42)
        
        # Test numpy float
        self.assertEqual(handle_numpy_types(np.float64(3.14)), 3.14)
        
        # Test numpy array
        arr = np.array([1, 2, 3])
        self.assertEqual(handle_numpy_types(arr), [1, 2, 3])
        
        # Test regular Python types
        self.assertEqual(handle_numpy_types(42), 42)
        self.assertEqual(handle_numpy_types(3.14), 3.14)
        self.assertEqual(handle_numpy_types([1, 2, 3]), [1, 2, 3])

    def test_create_error_response(self):
        response = create_error_response("Test error", 400)
        
        self.assertTrue(response["error"])
        self.assertEqual(response["message"], "Test error")
        self.assertEqual(response["status_code"], 400)
        self.assertIn("timestamp", response)

    def test_create_success_response(self):
        data = {"test": "data"}
        response = create_success_response(data, "Test success")
        
        self.assertFalse(response["error"])
        self.assertEqual(response["message"], "Test success")
        self.assertEqual(response["data"], data)
        self.assertIn("timestamp", response)

if __name__ == '__main__':
    unittest.main() 