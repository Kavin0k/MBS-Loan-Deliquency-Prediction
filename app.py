import os
import joblib
import pickle
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Define the model path
MODEL_FILENAME = "xgb_model.pkl"
model_path = os.path.join(os.path.dirname(__file__), MODEL_FILENAME)

# Check if model exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file '{MODEL_FILENAME}' not found in {os.getcwd()}")

# Load the model
model = joblib.load(model_path)

# Expected features
TRAINED_FEATURE_NAMES = ["CreditScore", "OrigUPB", "DTI", "LTV", "LoanAgeMonths", "DTI_per_Unit", "MonthlyPrincipal"]

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Model API is running!"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if not request.is_json:
            return jsonify({"error": "Invalid input, expecting JSON"}), 400

        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({"error": "Input should be a JSON object"}), 400

        # Convert input to DataFrame
        features = pd.DataFrame([data])

        # Check for missing features
        missing_features = [f for f in TRAINED_FEATURE_NAMES if f not in features.columns]
        if missing_features:
            return jsonify({"error": f"Missing features: {', '.join(missing_features)}"}), 400

        # Ensure correct feature order
        features = features[TRAINED_FEATURE_NAMES]

        # Convert to float
        features = features.astype(float)

        # Make prediction
        prediction = model.predict(features)

        return jsonify({"prediction": prediction.tolist()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
