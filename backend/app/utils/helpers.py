import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

def setup_logging(log_file: str, log_level: str = 'DEBUG') -> None:
    """Setup logging configuration"""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load and parse a JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading JSON file {file_path}: {str(e)}")
        raise

def save_json_file(data: Dict[str, Any], file_path: str) -> None:
    """Save data to a JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving JSON file {file_path}: {str(e)}")
        raise

def ensure_directory(directory: str) -> None:
    """Ensure a directory exists, create if it doesn't"""
    Path(directory).mkdir(parents=True, exist_ok=True)

def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """Format a timestamp as a string"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def sanitize_input(text: str) -> str:
    """Sanitize user input text"""
    # Remove any potentially harmful characters
    return text.strip()

def validate_symptoms(symptoms: List[str]) -> bool:
    """Validate symptoms list"""
    if not isinstance(symptoms, list):
        return False
    if not all(isinstance(s, str) and s.strip() for s in symptoms):
        return False
    return True

def format_prediction(prediction: Dict[str, float], top_n: int = 3) -> List[Dict[str, Any]]:
    """Format prediction results"""
    # Sort predictions by probability
    sorted_preds = sorted(
        prediction.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    # Take top N predictions
    top_preds = sorted_preds[:top_n]
    
    # Format results
    results = []
    for disease, prob in top_preds:
        results.append({
            'disease': disease,
            'probability': float(prob),  # Convert numpy float to Python float
            'percentage': f"{prob * 100:.1f}%"
        })
    
    return results

def handle_numpy_types(obj: Any) -> Any:
    """Convert numpy types to Python native types"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

def create_error_response(message: str, status_code: int = 400) -> Dict[str, Any]:
    """Create a standardized error response"""
    return {
        'error': True,
        'message': message,
        'status_code': status_code,
        'timestamp': format_timestamp()
    }

def create_success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
    """Create a standardized success response"""
    return {
        'error': False,
        'message': message,
        'data': data,
        'timestamp': format_timestamp()
    }

def validate_api_key(api_key: str, valid_keys: List[str]) -> bool:
    """Validate API key"""
    return api_key in valid_keys

def rate_limit_key(ip: str, endpoint: str) -> str:
    """Generate a rate limit key"""
    return f"{ip}:{endpoint}"

def get_client_ip(request) -> str:
    """Get client IP address from request"""
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.remote_addr 