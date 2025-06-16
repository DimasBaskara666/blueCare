import joblib
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)

class DiseasePredictor:
    def __init__(self, model_path: str):
        """Initialize the disease predictor with a trained model"""
        self.model = self._load_model(model_path)
        self.disease_mapping = {
            0: "Demam Berdarah",
            1: "Flu",
            2: "Gastritis",
            3: "Hipertensi",
            4: "Diabetes",
            5: "Asma",
            # Add more diseases as needed
        }
        
        # Common symptoms for each disease (to be expanded)
        self.disease_symptoms = {
            "Demam Berdarah": ["demam", "sakit_kepala", "nyeri_otot", "ruam"],
            "Flu": ["demam", "batuk", "pilek", "sakit_kepala", "lemas"],
            "Gastritis": ["mual", "muntah", "sakit_perut", "perut_kembung"],
            "Hipertensi": ["sakit_kepala", "pusing", "sesak_nafas"],
            "Diabetes": ["lemas", "sering_haus", "sering_kencing"],
            "Asma": ["sesak_nafas", "batuk", "dada_sesak"],
        }
        logger.info("DiseasePredictor initialized successfully")

    def _load_model(self, model_path: str):
        """Load the trained model from disk"""
        try:
            # Check if model file exists
            if not os.path.exists(model_path):
                logger.warning(f"Model file not found at {model_path}. Using dummy model.")
                return DummyModel()
            
            logger.info(f"Loading model from {model_path}")
            return joblib.load(model_path)
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            logger.warning("Using dummy model as fallback")
            return DummyModel()

    def _vectorize_symptoms(self, medical_terms: List[str]) -> np.ndarray:
        """Convert medical terms to feature vector"""
        try:
            # In a real implementation, this would use a proper vectorizer
            # For now, we'll use a simple binary vector
            all_symptoms = set()
            for symptoms in self.disease_symptoms.values():
                all_symptoms.update(symptoms)
            
            vector = np.zeros(len(all_symptoms))
            for i, symptom in enumerate(sorted(all_symptoms)):
                if symptom in medical_terms:
                    vector[i] = 1
            
            logger.debug(f"Vectorized symptoms: {vector}")
            return vector
        except Exception as e:
            logger.error(f"Error vectorizing symptoms: {str(e)}")
            raise

    def predict(self, medical_terms: List[str]) -> List[Dict[str, Any]]:
        """Predict diseases based on symptoms"""
        try:
            # Vectorize input
            features = self._vectorize_symptoms(medical_terms)
            logger.debug(f"Features shape: {features.shape}")
            
            # Get predictions
            if isinstance(self.model, DummyModel):
                logger.info("Using dummy model for predictions")
                predictions = self.model.predict(features)
            else:
                probabilities = self.model.predict_proba(features.reshape(1, -1))[0]
                predictions = []
                
                # Get top 3 predictions
                top_indices = np.argsort(probabilities)[-3:][::-1]
                for idx in top_indices:
                    if probabilities[idx] > 0.1:  # Only include if confidence > 10%
                        disease = self.disease_mapping[idx]
                        predictions.append({
                            "disease": disease,
                            "confidence": float(probabilities[idx]),
                            "symptoms": self.disease_symptoms[disease]
                        })
            
            logger.info(f"Generated predictions: {predictions}")
            return predictions
        except Exception as e:
            logger.error(f"Error making predictions: {str(e)}")
            raise

class DummyModel:
    """Dummy model for development and testing."""
    
    def __init__(self):
        self.classes_ = ["Flu", "Demam Berdarah", "Gastritis", "Hipertensi", "Diabetes", "Asma"]
        self.disease_symptoms = {
            "Flu": ["demam", "batuk", "pilek", "sakit_kepala", "lemas"],
            "Demam Berdarah": ["demam", "sakit_kepala", "nyeri_otot", "ruam"],
            "Gastritis": ["mual", "muntah", "sakit_perut", "perut_kembung"],
            "Hipertensi": ["sakit_kepala", "pusing", "sesak_nafas"],
            "Diabetes": ["lemas", "sering_haus", "sering_kencing"],
            "Asma": ["sesak_nafas", "batuk", "dada_sesak"]
        }
        logger.info("Initialized dummy model with classes: %s", self.classes_)
    
    def predict_proba(self, X):
        """Generate random probabilities for testing."""
        logger.debug("Generating dummy probabilities for input shape: %s", X.shape)
        # Generate random probabilities that sum to 1
        probs = np.random.dirichlet(np.ones(len(self.classes_)))
        return probs.reshape(1, -1)
    
    def predict(self, X):
        """Predict class labels and return formatted results."""
        logger.debug("Making dummy predictions for input shape: %s", X.shape)
        probs = self.predict_proba(X)[0]
        
        # Get top 3 predictions with confidence scores
        top_indices = np.argsort(probs)[-3:][::-1]
        predictions = []
        
        for idx in top_indices:
            if probs[idx] > 0.1:  # Only include if confidence > 10%
                disease = self.classes_[idx]
                predictions.append({
                    "disease": disease,
                    "confidence": float(probs[idx]),  # Convert numpy float to Python float
                    "symptoms": self.disease_symptoms.get(disease, [])
                })
        
        return predictions

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