import joblib
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)

print("=== Running NEW predictor.py version ===")

class DiseasePredictor:
    def __init__(self, model_path: str):
        """Initialize the disease predictor with a trained model pipeline"""
        self.model = self._load_model(model_path)
        logger.info("DiseasePredictor initialized successfully with trained pipeline")

    def _load_model(self, model_path: str):
        """Load the trained model pipeline from disk"""
        try:
            if not os.path.exists(model_path):
                logger.error(f"Model file not found at {model_path}. Prediction will not work.")
                raise FileNotFoundError(f"Model file not found at {model_path}")
            logger.info(f"Loading model pipeline from {model_path}")
            return joblib.load(model_path)
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def predict(self, medical_terms: List[str]) -> List[Dict[str, Any]]:
        """Predict diseases based on symptoms using the trained pipeline"""
        try:
            # Join symptoms into a single string for the vectorizer
            symptoms_text = ", ".join(medical_terms)
            logger.debug(f"Predicting for symptoms: {symptoms_text}")

            # Get class probabilities
            probabilities = self.model.predict_proba([symptoms_text])[0]
            classes = self.model.classes_
            predictions = []

            # Get top 3 predictions
            top_indices = np.argsort(probabilities)[-3:][::-1]
            for idx in top_indices:
                if probabilities[idx] > 0.1:  # Only include if confidence > 10%
                    disease = classes[idx]
                    predictions.append({
                        "disease": disease,
                        "confidence": float(probabilities[idx]),
                        "symptoms": []  # Optionally, map to known symptoms if you want
                    })

            logger.info(f"Generated predictions: {predictions}")
            return predictions
        except Exception as e:
            logger.error(f"Error making predictions: {str(e)}")
            raise

# Global predictor instance
_predictor = None

def initialize_predictor(model_path: str = "model/disease_classifier.pkl"):
    """Initialize the global predictor"""
    global _predictor
    if _predictor is None:
        logger.info("Initializing global predictor")
        _predictor = DiseasePredictor(model_path)
    return _predictor

def predict_disease(processed_text: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Predict disease using the global predictor"""
    global _predictor
    if _predictor is None:
        logger.info("Predictor not initialized, initializing now")
        _predictor = initialize_predictor()
    try:
        logger.debug(f"Making prediction for processed text: {processed_text}")
        return _predictor.predict(processed_text["medical_terms"])
    except Exception as e:
        logger.error(f"Error in predict_disease: {str(e)}")
        raise 