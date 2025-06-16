import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
from pathlib import Path
import os

DATA_PATH = Path(__file__).parent.parent / "data" / "symptom_disease_dataset.csv"
MODEL_DIR = Path(__file__).parent.parent / "model"
MODEL_PATH = MODEL_DIR / "disease_classifier.pkl"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"

os.makedirs(MODEL_DIR, exist_ok=True)

def main():
    # Load dataset
    df = pd.read_csv(DATA_PATH)
    X = df["symptoms"]
    y = df["disease"]

    # Split for evaluation (optional)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create pipeline: TF-IDF + Logistic Regression
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000, random_state=42))
    ])

    # Train
    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Save the full pipeline (recommended)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    # Optionally, save vectorizer separately
    joblib.dump(pipeline.named_steps["tfidf"], VECTORIZER_PATH)
    print(f"Vectorizer saved to {VECTORIZER_PATH}")

if __name__ == "__main__":
    main() 