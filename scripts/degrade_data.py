import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = pd.read_csv(ROOT / "data" / "iris_test.csv")

X = data.drop("target", axis=1)
y = data["target"]

# Add large noise to simulate data drift
np.random.seed(42)

noise = np.random.normal(
    loc=0,
    scale=2.0,
    size=X.shape
)

X_degraded = X + noise

degraded = X_degraded.copy()
degraded["target"] = y

degraded.to_csv(ROOT / "data" / "degraded_data.csv", index=False)

print("Degraded data created.")