import pandas as pd
import joblib
from sklearn.metrics import accuracy_score
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

model = joblib.load(ROOT / "models" / "production_model.pkl")

# Load degraded data
data = pd.read_csv(
    ROOT / "data" / "degraded_data.csv"
)

X = data.drop("target", axis=1)
y = data["target"]

# Predict
predictions = model.predict(X)

accuracy = accuracy_score(
    y,
    predictions
)

print("Current Model Accuracy:", accuracy)

# Save accuracy
with open(ROOT / "data" / "current_accuracy.txt", "w", encoding="utf-8") as f:
    f.write(str(accuracy))