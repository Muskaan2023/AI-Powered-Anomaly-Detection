import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

data = pd.read_csv(
    DATA_DIR / "final_dataset.csv"
)

print(data.head())
features = [
    "login_hour",
    "failed_login",
    "risk_score",
    "session_duration",
    "high_risk"
]
X = data[features]
from sklearn.ensemble import IsolationForest
model = IsolationForest(
    contamination=0.15,
    random_state=42
)
model.fit(X)
predictions = model.predict(X)
data["prediction"] = predictions

data.to_csv(
    DATA_DIR / "predictions.csv",
    index=False
)

print(data.head())