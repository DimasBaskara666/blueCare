import os
import sys
import logging
import nltk
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def download_nltk_data():
    """Download required NLTK data"""
    try:
        logger.info("Downloading NLTK data...")
        nltk.download('punkt')
        nltk.download('stopwords')
        logger.info("NLTK data downloaded successfully")
    except Exception as e:
        logger.error(f"Error downloading NLTK data: {str(e)}")
        raise

def create_directories():
    """Create necessary directories"""
    try:
        # Get the base directory
        base_dir = Path(__file__).resolve().parent.parent
        
        # Directories to create
        directories = [
            base_dir / 'logs',
            base_dir / 'models',
            base_dir / 'app' / 'tests' / '__pycache__',
            base_dir / 'app' / 'api' / '__pycache__',
            base_dir / 'app' / 'core' / '__pycache__',
            base_dir / 'app' / 'nlp' / '__pycache__',
            base_dir / 'app' / 'utils' / '__pycache__'
        ]
        
        # Create directories
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
        
        logger.info("All directories created successfully")
    except Exception as e:
        logger.error(f"Error creating directories: {str(e)}")
        raise

def create_env_file():
    """Create .env file from .env.example if it doesn't exist"""
    try:
        base_dir = Path(__file__).resolve().parent.parent
        env_example = base_dir / '.env.example'
        env_file = base_dir / '.env'
        
        if not env_file.exists() and env_example.exists():
            with open(env_example, 'r') as example:
                with open(env_file, 'w') as env:
                    env.write(example.read())
            logger.info("Created .env file from .env.example")
        elif not env_file.exists():
            logger.warning(".env.example not found, skipping .env creation")
    except Exception as e:
        logger.error(f"Error creating .env file: {str(e)}")
        raise

def initialize_app():
    """Initialize the application"""
    try:
        logger.info("Starting application initialization...")
        
        # Download NLTK data
        download_nltk_data()
        
        # Create directories
        create_directories()
        
        # Create .env file
        create_env_file()
        
        logger.info("Application initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing application: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    initialize_app() 