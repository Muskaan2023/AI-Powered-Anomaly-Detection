import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

logs = pd.read_csv(DATA_DIR / "attack_logs.csv")

logs["timestamp"] = pd.to_datetime(logs["timestamp"])

logs["login_hour"] = logs["timestamp"].dt.hour

logs["is_weekend"] = (
    logs["timestamp"].dt.dayofweek >= 5
).astype(int)

logs["session_length"] = logs["session_duration"]

logs["failed_login"] = (
    logs["login_status"] == "Failed"
).astype(int)

logs["high_risk"] = (
    logs["risk_score"] >= 80
).astype(int)

logs.to_csv(
    DATA_DIR / "final_dataset.csv",
    index=False
)

print(logs.head())