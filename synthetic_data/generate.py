import pandas as pd # type: ignore
import numpy as np # type: ignore
import random
from datetime import datetime, timedelta

# number of records
N = 5000

merchants = [
    "Amazon",
    "Walmart",
    "Target",
    "Apple",
    "Uber",
    "Netflix",
    "Airbnb",
    "Starbucks",
]

locations = [
    "New York",
    "London",
    "Delhi",
    "Berlin",
    "Tokyo",
    "Sydney",
]

devices = [
    "mobile",
    "web",
    "pos",
]

transaction_types = [
    "purchase",
    "withdrawal",
    "transfer",
]


def random_date():
    start = datetime(2023, 1, 1)
    end = datetime(2024, 12, 31)

    delta = end - start
    random_days = random.randint(0, delta.days)

    return start + timedelta(days=random_days)


data = []

for i in range(N):

    amount = round(np.random.exponential(scale=120), 2)

    fraud = 1 if random.random() < 0.03 else 0

    record = {
        "transaction_id": i,
        "amount": amount,
        "merchant": random.choice(merchants),
        "location": random.choice(locations),
        "device_type": random.choice(devices),
        "transaction_type": random.choice(transaction_types),
        "customer_age": random.randint(18, 75),
        "timestamp": random_date(),
        "fraud": fraud,
    }

    data.append(record)


df = pd.DataFrame(data)

df.to_csv("synthetic_data/transactions.csv", index=False)

print("Dataset generated successfully")
print(df.head())