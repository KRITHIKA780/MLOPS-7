from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Load Iris dataset
iris = load_iris()

X = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)
y = iris.target

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Initial Model Accuracy:", accuracy)

# Save model
os.makedirs(ROOT / "models", exist_ok=True)

joblib.dump(
    model,
    ROOT / "models" / "production_model.pkl"
)

# Save test data
test_data = pd.DataFrame(X_test)
test_data["target"] = y_test

os.makedirs("data", exist_ok=True)

test_data.to_csv(
    ROOT / "data" / "iris_test.csv",
    index=False
)

print("Production model saved.")