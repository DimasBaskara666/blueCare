from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # Enable CORS
    CORS(app)
    
    # Configure app
    app.config.from_mapping(
        SECRET_KEY="dev",
        MODEL_PATH="model/disease_classifier.pkl",
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    # Swagger documentation
    SWAGGER_URL = "/api/docs"
    API_URL = "/static/swagger.json"
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Disease Detection API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Initialize NLP components
    from .nlp_engine import initialize_nlp
    initialize_nlp()

    return app 