from pathlib import Path
import pandas as pd
import numpy as np
import random
from faker import Faker



BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
fake=Faker()

departments=[
    "HR",
    "Finance",
    "IT",
    "Sales",
    "Marketing"
]
cities=[
    "Delhi",
    "Mumbai",
    "Pune",
    "Bangalore",
    "Chennai",
    "Hyderbad"
]
operating_systems=[
    "Windows",
    "Linux",
    "macos"

]
browsers=[
    "Chrome",
    "Firefox",
    "Edge"
]
auth_methods=[
    "Password",
    "Biometric",
    "Token"
]
work_shifts=[
    ("09:00","18:00"),
    ("10:00","19:00"),
    ("08:00","17:00"),
    ("18:00","02:00")

]
department_resources={
    "HR":[
        "Email",
        "HR Portal",
        "Payroll"
    ],
    "Finance":[
        "Accounting",
        "Invoices",
        "Payroll"

    ],
    "IT":[
        "GitHub",
        "Jira",
        "Server"
    ],
    "Sales":[
        "CRM",
        "Customer Portal",
        "Email"
    ],
    "Marketing":[
        "Analytics",
        "Campaign Dashboard",
        "Email"
    ]
}

def create_users(number_of_users):
    users=[]
   
    for i in range(number_of_users):
        entity_id=f"Emp{i+1:03}"
        
        name=fake.name()
        department=random.choice(departments)
        resources = department_resources[department]
        city=random.choice(cities)
        operating_system=random.choice(operating_systems)
        browser=random.choice(browsers)
        auth_method=random.choice(auth_methods)
        login_time,logout_time=random.choice(work_shifts)
        
       
        user={
            "entity_id":entity_id,
            "name":name,
            "department":department,
            "city":city,
            "operating_system":operating_system,
            "browser":browser,
            "auth_method": auth_method,
            "login_time":login_time,
            "logout_time":logout_time,
            "resources":",".join(resources)

        }
        users.append(user)
    df=pd.DataFrame(users)
    df.to_csv(DATA_DIR / "users.csv", index=False)
    return df
if __name__=="__main__":
    create_users(1000)




