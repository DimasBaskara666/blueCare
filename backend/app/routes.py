from flask import Blueprint, jsonify, request
from .nlp_engine import process_symptoms
from .predictor import predict_disease
from .chatbot import get_chatbot_response
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

main_bp = Blueprint("main", __name__)

@main_bp.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "API is running"})

@main_bp.route("/api/predict", methods=["POST"])
def predict():
    """
    Predict disease based on symptoms
    ---
    parameters:
      - name: symptoms
        in: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              description: Description of symptoms in Bahasa Indonesia
    responses:
      200:
        description: Prediction results
        schema:
          type: object
          properties:
            predictions:
              type: array
              items:
                type: object
                properties:
                  disease:
                    type: string
                  confidence:
                    type: number
                  symptoms:
                    type: array
                    items:
                      type: string
    """
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "No symptoms provided"}), 400

        logger.debug(f"Received symptoms: {data['text']}")
        
        # Process the input text
        processed_text = process_symptoms(data["text"])
        logger.debug(f"Processed text: {processed_text}")
        
        # Get predictions
        predictions = predict_disease(processed_text)
        logger.debug(f"Predictions: {predictions}")
        
        return jsonify({
            "predictions": predictions,
            "processed_text": processed_text
        })
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e), "details": traceback.format_exc()}), 500

@main_bp.route("/api/chat", methods=["POST"])
def chat():
    """
    Chat with the health assistant
    ---
    parameters:
      - name: message
        in: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              description: User message
            context:
              type: object
              description: Chat context/history
    responses:
      200:
        description: Chatbot response
        schema:
          type: object
          properties:
            response:
              type: string
            suggestions:
              type: array
              items:
                type: string
    """
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "No message provided"}), 400

        response = get_chatbot_response(
            data["text"],
            context=data.get("context", {})
        )
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500 