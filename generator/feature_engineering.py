import pandas as pd
logs=pd.read_csv("D:/AI-Powered-Anomaly-Detection/data/attack_logs.csv")

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
"D:/AI-Powered-Anomaly-Detection/data/final_dataset.csv",
index=False
)

print(logs.head())