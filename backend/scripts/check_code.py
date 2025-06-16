import os
import sys
import subprocess
import logging
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Run a shell command and log the output"""
    try:
        logger.info(f"Running {description}...")
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        logger.info(f"{description} completed successfully")
        if result.stdout:
            logger.info(f"{description} output:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"{description} failed with error:\n{e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error running {description}: {str(e)}")
        return False

def run_black():
    """Run black code formatter"""
    return run_command(
        "black .",
        "Black code formatting"
    )

def run_flake8():
    """Run flake8 linter"""
    return run_command(
        "flake8 .",
        "Flake8 linting"
    )

def run_isort():
    """Run isort import sorter"""
    return run_command(
        "isort .",
        "isort import sorting"
    )

def run_mypy():
    """Run mypy type checker"""
    return run_command(
        "mypy .",
        "mypy type checking"
    )

def check_code():
    """Run all code quality checks"""
    try:
        logger.info("Starting code quality checks...")
        
        # Run all checks
        checks = [
            (run_black, "Black"),
            (run_flake8, "Flake8"),
            (run_isort, "isort"),
            (run_mypy, "mypy")
        ]
        
        # Track results
        results = []
        for check_func, name in checks:
            success = check_func()
            results.append((name, success))
        
        # Log summary
        logger.info("\nCode Quality Check Summary:")
        all_passed = True
        for name, success in results:
            status = "PASSED" if success else "FAILED"
            logger.info(f"{name}: {status}")
            if not success:
                all_passed = False
        
        if all_passed:
            logger.info("All code quality checks passed!")
            return 0
        else:
            logger.error("Some code quality checks failed!")
            return 1
            
    except Exception as e:
        logger.error(f"Error running code quality checks: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(check_code()) 