import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

print("Loading dataset...")
data = pd.read_csv("data/dummy_data.csv")

# Features and Labels
X = data[["heart_rate", "temperature", "motion", "voice_panic_score"]]
y = data["label"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Random Forest Classifier...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {acc:.4f}\n")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save the model
os.makedirs('ml', exist_ok=True)
joblib.dump(model, "ml/model.pkl")

print("Supervised model training complete and saved to ml/model.pkl")
