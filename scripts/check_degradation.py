import sys
from pathlib import Path

THRESHOLD = 0.80
ROOT = Path(__file__).resolve().parents[1]

with open(ROOT / "data" / "current_accuracy.txt", "r", encoding="utf-8") as f:
    accuracy = float(f.read())

print("Current Accuracy:", accuracy)
print("Required Accuracy:", THRESHOLD)

if accuracy < THRESHOLD:

    print("Performance degradation detected!")
    print("Retraining is required.")

    sys.exit(0)

else:

    print("Model performance is acceptable.")
    print("Retraining is not required.")

    sys.exit(1)