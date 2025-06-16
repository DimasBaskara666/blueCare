import os
import sys
import logging
import subprocess
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_gunicorn():
    """Run the application using gunicorn"""
    try:
        # Get configuration from environment variables
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 5000))
        workers = int(os.getenv('GUNICORN_WORKERS', 4))
        timeout = int(os.getenv('GUNICORN_TIMEOUT', 120))
        
        # Build gunicorn command
        cmd = [
            'gunicorn',
            f'--bind={host}:{port}',
            f'--workers={workers}',
            f'--timeout={timeout}',
            '--access-logfile=-',
            '--error-logfile=-',
            '--log-level=info',
            '--worker-class=sync',
            '--preload',
            'scripts.run_app:create_app()'
        ]
        
        logger.info(f"Starting gunicorn with {workers} workers on {host}:{port}")
        logger.info(f"Command: {' '.join(cmd)}")
        
        # Run gunicorn
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error running gunicorn: {str(e)}")
        sys.exit(1)

def check_environment():
    """Check if the environment is properly configured for production"""
    try:
        # Check if DEBUG is False
        if os.getenv('DEBUG', 'True').lower() == 'true':
            logger.warning("DEBUG mode is enabled. This is not recommended for production.")
        
        # Check if SECRET_KEY is set
        if not os.getenv('SECRET_KEY'):
            logger.error("SECRET_KEY is not set. This is required for production.")
            return False
        
        # Check if CORS_ORIGINS is set
        if not os.getenv('CORS_ORIGINS'):
            logger.warning("CORS_ORIGINS is not set. This may cause CORS issues.")
        
        # Check if required directories exist
        base_dir = Path(__file__).resolve().parent.parent
        required_dirs = [
            base_dir / 'logs',
            base_dir / 'models'
        ]
        
        for directory in required_dirs:
            if not directory.exists():
                logger.error(f"Required directory does not exist: {directory}")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error checking environment: {str(e)}")
        return False

def run_production():
    """Run the application in production mode"""
    try:
        logger.info("Starting production mode...")
        
        # Check environment
        if not check_environment():
            logger.error("Environment check failed. Please fix the issues before running in production.")
            sys.exit(1)
        
        # Run gunicorn
        run_gunicorn()
        
    except Exception as e:
        logger.error(f"Error in production mode: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    run_production() 