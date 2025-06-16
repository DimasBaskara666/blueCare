import unittest
from unittest.mock import patch, MagicMock
import json
from flask import Flask
from app.api.routes import api_bp

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(api_bp)
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = self.client.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)

    @patch('app.api.routes.predict_disease')
    def test_predict_endpoint_success(self, mock_predict):
        """Test the predict endpoint with valid input"""
        # Mock the prediction function
        mock_predict.return_value = {
            "Flu": 0.6,
            "Common Cold": 0.3,
            "COVID-19": 0.1
        }
        
        # Test data
        test_data = {
            "symptoms": ["demam", "batuk", "sakit kepala"]
        }
        
        response = self.client.post(
            '/predict',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['error'])
        self.assertIn('predictions', data['data'])
        self.assertEqual(len(data['data']['predictions']), 3)

    def test_predict_endpoint_invalid_input(self):
        """Test the predict endpoint with invalid input"""
        # Test with missing symptoms
        test_data = {}
        
        response = self.client.post(
            '/predict',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertIn('message', data)

    @patch('app.api.routes.get_chatbot_response')
    def test_chat_endpoint_success(self, mock_chat):
        """Test the chat endpoint with valid input"""
        # Mock the chatbot response
        mock_chat.return_value = {
            "response": "Halo! Apa yang bisa saya bantu?",
            "suggestions": [
                "Apakah ada gejala lain?",
                "Sudah berapa lama gejala ini berlangsung?"
            ]
        }
        
        # Test data
        test_data = {
            "message": "halo",
            "context": {}
        }
        
        response = self.client.post(
            '/chat',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['error'])
        self.assertIn('response', data['data'])
        self.assertIn('suggestions', data['data'])

    def test_chat_endpoint_invalid_input(self):
        """Test the chat endpoint with invalid input"""
        # Test with missing message
        test_data = {
            "context": {}
        }
        
        response = self.client.post(
            '/chat',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertIn('message', data)

    def test_predict_endpoint_malformed_json(self):
        """Test the predict endpoint with malformed JSON"""
        response = self.client.post(
            '/predict',
            data='invalid json',
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertIn('message', data)

    def test_chat_endpoint_malformed_json(self):
        """Test the chat endpoint with malformed JSON"""
        response = self.client.post(
            '/chat',
            data='invalid json',
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertIn('message', data)

    @patch('app.api.routes.predict_disease')
    def test_predict_endpoint_empty_symptoms(self, mock_predict):
        """Test the predict endpoint with empty symptoms list"""
        test_data = {
            "symptoms": []
        }
        
        response = self.client.post(
            '/predict',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertIn('message', data)

    @patch('app.api.routes.get_chatbot_response')
    def test_chat_endpoint_empty_message(self, mock_chat):
        """Test the chat endpoint with empty message"""
        test_data = {
            "message": "",
            "context": {}
        }
        
        response = self.client.post(
            '/chat',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 400)
        self.assertTrue(data['error'])
        self.assertIn('message', data)

if __name__ == '__main__':
    unittest.main() 