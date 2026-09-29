import shutil
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

production_model = ROOT / "models" / "production_model.pkl"
new_model = ROOT / "models" / "new_model.pkl"


if os.path.exists(new_model):

    shutil.copyfile(
        new_model,
        production_model
    )

    print("New model deployed successfully.")
    print("Production model replaced.")

else:

    print("New model not found.")