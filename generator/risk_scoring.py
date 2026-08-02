import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

data = pd.read_csv(DATA_DIR / "predictions.csv")

def calculate_risk(row):

    score = 0
    if row["prediction"] == -1:
        score += 40

    if row["failed_login"] == 1:
        score += 20

    if row["high_risk"] == 1:
        score += 20

    if row["risk_score"] >= 80:
        score += 20

    return score

data["final_risk_score"] = data.apply(
    calculate_risk,
    axis=1
)

def severity(score):

    if score >= 80:
        return "High"

    elif score >= 50:
        return "Medium"

    else:
        return "Low"

data["severity"] = data["final_risk_score"].apply(severity)

data.to_csv(
    DATA_DIR /"final_results.csv",
    index=False
)

print(data.head())