import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Read users dataset
users = pd.read_csv(DATA_DIR / "users.csv")

fake = Faker()

logs = []
session_counter = 1

# Starting date
base_date = datetime(2026, 7, 1)

# Loop through every user
for index, user in users.iterrows():

    # Generate logs for 30 days
    for day in range(30):

        session_id = f"sess_{session_counter:06}"

        entity_id = user["entity_id"]
        department = user["department"]
        city = user["city"]
        browser = user["browser"]
        operating_system = user["operating_system"]
        auth_method = user["auth_method"]
        resources = user["resources"]

        # Convert resources string into list
        resource_list = resources.split(",")

        # Login time
        login_time = user["login_time"]
        login_datetime = datetime.strptime(login_time, "%H:%M")

        current_date = base_date + timedelta(days=day)

        login_timestamp = current_date.replace(
            hour=login_datetime.hour,
            minute=login_datetime.minute,
            second=0
        )

        # Random delay
        login_timestamp += timedelta(minutes=random.randint(-10, 10))

        source_ip = fake.ipv4()
        session_duration = random.randint(20, 120)

        device_id = f"DEV-{random.randint(1000,9999)}"

        # ---------------- LOGIN EVENT ----------------
        login_event = {
            "session_id": session_id,
            "entity_id": entity_id,
            "department": department,
            "timestamp": login_timestamp,
            "event_type": "Login",
            "source_ip": source_ip,
            "geo_location": city,
            "operating_system": operating_system,
            "browser": browser,
            "device_id": device_id,
            "auth_method": auth_method,
            "resource_accessed": "-",
            "session_duration": session_duration,
            "login_status": "Success",
            "risk_score": 0,
            "label": "Normal"
        }

        logs.append(login_event)

        # ---------------- RESOURCE EVENTS ----------------
        event_time = login_timestamp

        for resource in resource_list:

            # Each resource is accessed a few minutes later
            event_time += timedelta(minutes=random.randint(2, 8))

            resource_event = {
                "session_id": session_id,
                "entity_id": entity_id,
                "department": department,
                "timestamp": event_time,
                "event_type": "Resource Access",
                "source_ip": source_ip,
                "geo_location": city,
                "operating_system": operating_system,
                "browser": browser,
                "device_id": device_id,
                "auth_method": auth_method,
                "resource_accessed": resource,
                "session_duration": session_duration,
                "login_status": "Success",
                "risk_score": 0,
                "label": "Normal"
            }

            logs.append(resource_event)

        # ---------------- LOGOUT EVENT ----------------
        logout_time = login_timestamp + timedelta(minutes=session_duration)

        logout_event = {
            "session_id": session_id,
            "entity_id": entity_id,
            "department": department,
            "timestamp": logout_time,
            "event_type": "Logout",
            "source_ip": source_ip,
            "geo_location": city,
            "operating_system": operating_system,
            "browser": browser,
            "device_id": device_id,
            "auth_method": auth_method,
            "resource_accessed": "-",
            "session_duration": session_duration,
            "login_status": "Success",
            "risk_score": 0,
            "label": "Normal"
        }

        logs.append(logout_event)

        session_counter += 1

# Save dataset
df_logs = pd.DataFrame(logs)

df_logs.to_csv(
    DATA_DIR / "normal_logs.csv",
    index=False
)

print(df_logs.head())
print(f"\nTotal Events Generated: {len(df_logs)}")
    