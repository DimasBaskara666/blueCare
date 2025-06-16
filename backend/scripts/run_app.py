import os
import sys
import logging
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from config.settings import (
    DEBUG,
    SECRET_KEY,
    CORS_ORIGINS,
    CORS_METHODS,
    CORS_HEADERS,
    LOG_LEVEL,
    LOG_FORMAT,
    LOG_FILE
)

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure the Flask application"""
    # Create Flask app
    app = Flask(__name__)
    
    # Configure app
    app.config['DEBUG'] = DEBUG
    app.config['SECRET_KEY'] = SECRET_KEY
    
    # Configure CORS
    CORS(
        app,
        resources={r"/*": {
            "origins": CORS_ORIGINS,
            "methods": CORS_METHODS,
            "allow_headers": CORS_HEADERS
        }}
    )
    
    # Register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Initialize components
    from app.core.predictor import initialize_predictor
    from app.core.chatbot import initialize_chatbot
    from app.nlp.engine import NLPEngine
    
    try:
        initialize_predictor()
        initialize_chatbot()
        nlp_engine = NLPEngine()
        logger.info("All components initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing components: {str(e)}")
        raise
    
    return app

def run_app():
    """Run the Flask application"""
    try:
        app = create_app()
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        
        logger.info(f"Starting application on {host}:{port}")
        app.run(host=host, port=port)
    except Exception as e:
        logger.error(f"Error running application: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    run_app() 