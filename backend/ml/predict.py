import joblib
import numpy as np
import time

# Load the trained Random Forest model
model = joblib.load("ml/model.pkl")

PANIC_KEYWORDS = ["help", "aaaah", "ahhh", "stop", "scream"]

def get_voice_score(voice_text):
    if not voice_text:
        return 0
    text_lower = voice_text.lower().strip()
    for word in PANIC_KEYWORDS:
        if word in text_lower:
            return 1
    return 0

def predict_risk(data):
    # Extract features from incoming API payload
    heart_rate = data.get("heart_rate", 80)
    temperature = data.get("temperature", 36.8)
    motion = data.get("motion", 1)
    voice_text = data.get("voice", "")
    
    # Preprocess text to numeric score
    voice_score = get_voice_score(voice_text)
    
    # Model expects: [heart_rate, temperature, motion, voice_panic_score]
    X = np.array([[heart_rate, temperature, motion, voice_score]])
    
    # Predict using the trained Random Forest Classifier
    prediction = model.predict(X)[0]
    
    return prediction  # Returns "SAFE", "EXERCISE", or "PANIC"
