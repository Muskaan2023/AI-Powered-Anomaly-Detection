import pandas as pd
import random
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

logs = pd.read_csv(DATA_DIR / "normal_logs.csv")
attack_logs=logs.copy()
attack_count=int(len(attack_logs)*0.15)
attack_indices=random.sample(range(len(attack_logs)),attack_count)
attack_logs["attack_type"] = "None"
attack_logs["failed_attempts"] = 0
attack_logs["risk_score"] = 0


attack_catalog = {
    "Brute Force": {
        "risk": (80, 90),
        "failed_attempts": (15, 25)
    },
    "Credential Stuffing": {
        "risk": (85, 95),
        "failed_attempts": (10, 20)
    },
    "Impossible Travel": {
        "risk": (85, 95),
        "failed_attempts": (0, 2)
    },
    "VPN Login": {
        "risk": (60, 75),
        "failed_attempts": (0, 1)
    },
    "Malware": {
        "risk": (90, 100),
        "failed_attempts": (0, 3)
    },
    "Privilege Escalation": {
        "risk": (90, 100),
        "failed_attempts": (1, 5)
    },
    "Data Exfiltration": {
        "risk": (95, 100),
        "failed_attempts": (0, 2)
    }
}

for index in attack_indices:

    # Select a random attack
    attack = random.choice(list(attack_catalog.keys()))

    attack_logs.loc[index, "attack_type"] = attack

    # Get risk range
    risk_low, risk_high = attack_catalog[attack]["risk"]

    attack_logs.loc[index, "risk_score"] = random.randint(
        risk_low,
        risk_high
    )

    # Get failed attempts range
    fail_low, fail_high = attack_catalog[attack]["failed_attempts"]

    attack_logs.loc[index, "failed_attempts"] = random.randint(
        fail_low,
        fail_high
    )

    attack_logs.loc[index, "login_status"] = "Failed"

    attack_logs.loc[index, "label"] = "Attack"
attack_logs.to_csv(DATA_DIR / "attack_logs.csv", index=False)
print(attack_logs.head())
print("Total Events:", len(attack_logs))
print("Attack Events:", attack_count)
print("Normal Events:", len(attack_logs) - attack_count)

