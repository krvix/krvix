import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Any
import joblib
import os
from src.config.settings import MODEL_PATH, PREDICTION_THRESHOLD


class SupplyChainPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self._load_model()

    def _load_model(self):
        model_file = os.path.join(MODEL_PATH, "supply_chain_model.h5")
        scaler_file = os.path.join(MODEL_PATH, "scaler.pkl")

        if os.path.exists(model_file) and os.path.exists(scaler_file):
            self.model = tf.keras.models.load_model(model_file)
            self.scaler = joblib.load(scaler_file)

    def train_model(self, training_data: pd.DataFrame):
        # Prepare features and labels
        features = training_data.drop(["target"], axis=1)
        labels = training_data["target"]

        # Scale features
        self.scaler = StandardScaler()
        scaled_features = self.scaler.fit_transform(features)

        # Define model architecture
        self.model = tf.keras.Sequential(
            [
                tf.keras.layers.Dense(
                    64, activation="relu", input_shape=(features.shape[1],)
                ),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(32, activation="relu"),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(16, activation="relu"),
                tf.keras.layers.Dense(1, activation="sigmoid"),
            ]
        )

        # Compile model
        self.model.compile(
            optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]
        )

        # Train model
        self.model.fit(
            scaled_features, labels, epochs=50, batch_size=32, validation_split=0.2
        )

        # Save model and scaler
        os.makedirs(MODEL_PATH, exist_ok=True)
        self.model.save(os.path.join(MODEL_PATH, "supply_chain_model.h5"))
        joblib.dump(self.scaler, os.path.join(MODEL_PATH, "scaler.pkl"))

    def predict_bottlenecks(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        if self.model is None or self.scaler is None:
            raise ValueError("Model not trained. Please train the model first.")

        # Scale features
        scaled_data = self.scaler.transform(data)

        # Make predictions
        predictions = self.model.predict(scaled_data)

        # Process predictions
        results = []
        for idx, prob in enumerate(predictions):
            if prob[0] > PREDICTION_THRESHOLD:
                results.append(
                    {
                        "index": idx,
                        "probability": float(prob[0]),
                        "data": data.iloc[idx].to_dict(),
                    }
                )

        return results

    def predict_demand(self, historical_data: pd.DataFrame) -> Dict[str, Any]:
        if self.model is None or self.scaler is None:
            raise ValueError("Model not trained. Please train the model first.")

        # Prepare time series data
        scaled_data = self.scaler.transform(historical_data)

        # Make predictions
        forecast = self.model.predict(scaled_data)

        return {
            "forecast": forecast.tolist(),
            "confidence_score": self._calculate_confidence_score(forecast),
        }

    def _calculate_confidence_score(self, predictions: np.ndarray) -> float:
        # Simple confidence score based on prediction variance
        return float(1.0 - np.var(predictions))
