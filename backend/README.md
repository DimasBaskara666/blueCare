# Disease Detection System Backend

This is the backend service for the Disease Detection System, built with Flask and using NLP for processing Indonesian medical text.

## Features

- Disease prediction based on symptoms
- Health assistant chatbot
- NLP processing for Indonesian medical text
- RESTful API endpoints
- Comprehensive test suite
- Logging and error handling
- CORS support
- Rate limiting
- API documentation

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- virtualenv (recommended)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Download required NLTK data:

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Configuration

The application can be configured using environment variables or by modifying the settings in `config/settings.py`. Key configuration options include:

- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Application secret key
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)
- `LOG_LEVEL`: Logging level (default: DEBUG)
- `CORS_ORIGINS`: Allowed CORS origins

## Running the Application

1. Start the development server:

```bash
python scripts/run_app.py
```

2. For production deployment:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "scripts.run_app:create_app()"
```

## Running Tests

Run the test suite:

```bash
python scripts/run_tests.py
```

For test coverage report:

```bash
pytest --cov=app tests/
```

## API Endpoints

### Health Check

- `GET /api/health`
- Returns the API health status

### Disease Prediction

- `POST /api/predict`
- Request body:

```json
{
  "symptoms": ["demam", "batuk", "sakit kepala"]
}
```

- Returns predicted diseases with probabilities

### Health Assistant Chat

- `POST /api/chat`
- Request body:

```json
{
  "message": "Saya mengalami demam",
  "context": {}
}
```

- Returns chatbot response and suggestions

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes.py
│   │
│   │   └── routes.py
│   ├── core/
│   │   ├── predictor.py
│   │   └── chatbot.py
│   ├── nlp/
│   │   └── engine.py
│   ├── utils/
│   │   └── helpers.py
│   └── tests/
│       ├── test_api.py
│       ├── test_core.py
│       ├── test_nlp.py
│       └── test_utils.py
├── config/
│   └── settings.py
├── scripts/
│   ├── run_app.py
│   └── run_tests.py
├── logs/
├── models/
├── requirements.txt
└── README.md
```

## Development

### Code Style

The project uses:

- Black for code formatting
- Flake8 for linting
- isort for import sorting
- mypy for type checking

Run code quality checks:

```bash
black .
flake8
isort .
mypy .
```

### Adding New Features

1. Create feature branch
2. Implement changes
3. Add tests
4. Run test suite
5. Submit pull request

## Error Handling

The application includes comprehensive error handling:

- Input validation
- Exception logging
- Standardized error responses
- Rate limiting
- CORS protection

## Logging

Logs are written to both console and file (`logs/app.log`). Log levels:

- DEBUG: Detailed information
- INFO: General information
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
