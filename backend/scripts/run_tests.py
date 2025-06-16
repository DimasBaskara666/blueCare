import unittest
import sys
import os
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

def run_tests():
    """Run all tests in the application"""
    # Get the directory containing this script
    script_dir = Path(__file__).resolve().parent
    # Get the app directory
    app_dir = script_dir.parent / 'app'
    # Get the tests directory
    tests_dir = app_dir / 'tests'
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = str(tests_dir)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Log the results
    logger.info(f"Ran {result.testsRun} tests")
    if result.wasSuccessful():
        logger.info("All tests passed successfully!")
    else:
        logger.error("Some tests failed!")
        for error in result.errors:
            logger.error(f"Error in {error[0]}: {error[1]}")
        for failure in result.failures:
            logger.error(f"Failure in {failure[0]}: {failure[1]}")
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    try:
        sys.exit(run_tests())
    except Exception as e:
        logger.error(f"Error running tests: {str(e)}")
        sys.exit(1) 