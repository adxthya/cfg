from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import cv2
import xgboost as xgb
import os

app = Flask(__name__)
CORS(app)  # Allow requests from the frontend

# Load trained model and scaler
# if os.path.exists("fetal_health_model.pkl"):  
#     model = xgb.Booster()
#     model.load_model("fetal_health_model.pkl")  # Load XGBoost Model
#     is_xgboost = True
# else:
model = joblib.load("fetal_health_model.pkl")  # Load other models
is_xgboost = False

scaler = joblib.load("scaler.pkl")  # Load scaler

# Function to extract features from the waveform image
def extract_features_from_waveform(image):
    try:
        # Convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Resize to a standard size (ensure consistent input)
        resized = cv2.resize(gray, (100, 100))  # Adjust size as needed
        
        # Extract meaningful features (customize this part)
        mean_intensity = np.mean(resized)
        std_dev = np.std(resized)
        
        # Dummy placeholder for additional extracted features
        additional_features = np.random.rand(20)  # Replace with actual features
        
        features = np.hstack([mean_intensity, std_dev, additional_features])
        return features
    except Exception as e:
        return None

@app.route("/predict/manual", methods=["POST"])
def predict_manual():
    try:
        data = request.json
        # features = np.array(data["features"]).reshape(1, -1)
        # features_scaled = scaler.transform(features)


        # prediction = model.predict(features_scaled)
        # result = {0: "Normal", 1: "Suspect", 2: "Pathological"}[int(prediction[0])]

        baseline = float(data.get("baseline", 0))

        if baseline < 100:
            result = "Normal"
        elif 100 <= baseline <= 200:
            result = "Suspect"
        else:
            result = "Pathological"

        print(result)
        return jsonify({"prediction": result})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

@app.route("/predict/image", methods=["POST"])
def predict_image():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

        features = extract_features_from_waveform(image)
        if features is None:
            return jsonify({"error": "Failed to extract features from image"}), 400

        features_scaled = scaler.transform([features])

        if is_xgboost:
            dmatrix = xgb.DMatrix(features_scaled)
            prediction = model.predict(dmatrix)
            prediction = np.round(prediction).astype(int)  # Convert probabilities to class labels
        else:
            prediction = model.predict(features_scaled)

        result = {0: "Normal", 1: "Suspect", 2: "Pathological"}[prediction[0]]
        return jsonify({"prediction": result})

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
