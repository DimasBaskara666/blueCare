import unittest
import json
import os
import tempfile
from datetime import datetime
import numpy as np
from app.utils.helpers import (
    setup_logging,
    load_json_file,
    save_json_file,
    ensure_directory,
    format_timestamp,
    sanitize_input,
    validate_symptoms,
    format_prediction,
    handle_numpy_types,
    create_error_response,
    create_success_response,
    validate_api_key,
    rate_limit_key,
    get_client_ip
)

class TestHelpers(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_log_file = os.path.join(self.test_dir, 'test.log')
        self.test_json_file = os.path.join(self.test_dir, 'test.json')

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)
        if os.path.exists(self.test_json_file):
            os.remove(self.test_json_file)
        os.rmdir(self.test_dir)

    def test_setup_logging(self):
        """Test logging setup"""
        setup_logging(self.test_log_file, 'DEBUG')
        
        # Check if log file was created
        self.assertTrue(os.path.exists(self.test_log_file))
        
        # Test invalid log level
        with self.assertRaises(ValueError):
            setup_logging(self.test_log_file, 'INVALID_LEVEL')

    def test_json_file_operations(self):
        """Test JSON file operations"""
        test_data = {
            'test': 'data',
            'number': 42,
            'list': [1, 2, 3]
        }
        
        # Test saving JSON file
        save_json_file(test_data, self.test_json_file)
        self.assertTrue(os.path.exists(self.test_json_file))
        
        # Test loading JSON file
        loaded_data = load_json_file(self.test_json_file)
        self.assertEqual(loaded_data, test_data)
        
        # Test loading non-existent file
        with self.assertRaises(Exception):
            load_json_file('nonexistent.json')

    def test_ensure_directory(self):
        """Test directory creation"""
        test_dir = os.path.join(self.test_dir, 'test_subdir')
        
        # Test creating new directory
        ensure_directory(test_dir)
        self.assertTrue(os.path.exists(test_dir))
        self.assertTrue(os.path.isdir(test_dir))
        
        # Test creating existing directory (should not raise error)
        ensure_directory(test_dir)

    def test_format_timestamp(self):
        """Test timestamp formatting"""
        # Test with current time
        timestamp = format_timestamp()
        self.assertIsInstance(timestamp, str)
        self.assertEqual(len(timestamp), 19)  # YYYY-MM-DD HH:MM:SS
        
        # Test with specific datetime
        test_time = datetime(2024, 1, 1, 12, 0, 0)
        timestamp = format_timestamp(test_time)
        self.assertEqual(timestamp, "2024-01-01 12:00:00")

    def test_sanitize_input(self):
        """Test input sanitization"""
        # Test with normal text
        text = "  Hello World  "
        sanitized = sanitize_input(text)
        self.assertEqual(sanitized, "Hello World")
        
        # Test with empty string
        self.assertEqual(sanitize_input(""), "")
        
        # Test with whitespace only
        self.assertEqual(sanitize_input("   "), "")

    def test_validate_symptoms(self):
        """Test symptoms validation"""
        # Test valid symptoms
        valid_symptoms = ["demam", "batuk", "sakit kepala"]
        self.assertTrue(validate_symptoms(valid_symptoms))
        
        # Test invalid symptoms (not a list)
        self.assertFalse(validate_symptoms("demam"))
        
        # Test invalid symptoms (empty strings)
        self.assertFalse(validate_symptoms(["demam", "", "batuk"]))
        
        # Test empty list
        self.assertFalse(validate_symptoms([]))

    def test_format_prediction(self):
        """Test prediction formatting"""
        prediction = {
            "Flu": 0.6,
            "Common Cold": 0.3,
            "COVID-19": 0.1
        }
        
        # Test with default top_n
        formatted = format_prediction(prediction)
        self.assertEqual(len(formatted), 3)
        self.assertEqual(formatted[0]["disease"], "Flu")
        self.assertEqual(formatted[0]["probability"], 0.6)
        self.assertEqual(formatted[0]["percentage"], "60.0%")
        
        # Test with custom top_n
        formatted = format_prediction(prediction, top_n=2)
        self.assertEqual(len(formatted), 2)
        self.assertEqual(formatted[0]["disease"], "Flu")
        self.assertEqual(formatted[1]["disease"], "Common Cold")

    def test_handle_numpy_types(self):
        """Test numpy type handling"""
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
        """Test error response creation"""
        response = create_error_response("Test error", 400)
        
        self.assertTrue(response["error"])
        self.assertEqual(response["message"], "Test error")
        self.assertEqual(response["status_code"], 400)
        self.assertIn("timestamp", response)

    def test_create_success_response(self):
        """Test success response creation"""
        data = {"test": "data"}
        response = create_success_response(data, "Test success")
        
        self.assertFalse(response["error"])
        self.assertEqual(response["message"], "Test success")
        self.assertEqual(response["data"], data)
        self.assertIn("timestamp", response)

    def test_validate_api_key(self):
        """Test API key validation"""
        valid_keys = ["key1", "key2", "key3"]
        
        # Test valid key
        self.assertTrue(validate_api_key("key1", valid_keys))
        
        # Test invalid key
        self.assertFalse(validate_api_key("invalid_key", valid_keys))
        
        # Test empty key
        self.assertFalse(validate_api_key("", valid_keys))

    def test_rate_limit_key(self):
        """Test rate limit key generation"""
        ip = "127.0.0.1"
        endpoint = "/api/predict"
        
        key = rate_limit_key(ip, endpoint)
        self.assertEqual(key, f"{ip}:{endpoint}")

    def test_get_client_ip(self):
        """Test client IP extraction"""
        # Mock request object
        class MockRequest:
            def __init__(self, headers=None, remote_addr=None):
                self.headers = headers or {}
                self.remote_addr = remote_addr or "127.0.0.1"
        
        # Test with X-Forwarded-For header
        request = MockRequest(headers={"X-Forwarded-For": "192.168.1.1, 10.0.0.1"})
        self.assertEqual(get_client_ip(request), "192.168.1.1")
        
        # Test without X-Forwarded-For header
        request = MockRequest()
        self.assertEqual(get_client_ip(request), "127.0.0.1")

if __name__ == '__main__':
    unittest.main() 