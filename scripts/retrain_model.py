from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


print("Starting model retraining...")


# Load fresh Iris dataset
iris = load_iris()

X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = iris.target


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=100,
    stratify=y
)


# Train new model
new_model = RandomForestClassifier(
    n_estimators=100,
    random_state=100
)

new_model.fit(X_train, y_train)


# Evaluate new model
predictions = new_model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("New Model Accuracy:", accuracy)


# Create models directory
os.makedirs(ROOT / "models", exist_ok=True)


# Save new model
joblib.dump(
    new_model,
    ROOT / "models" / "new_model.pkl"
)


# Save accuracy
with open(ROOT / "data" / "new_accuracy.txt", "w", encoding="utf-8") as f:
    f.write(str(accuracy))


print("New model saved successfully.")