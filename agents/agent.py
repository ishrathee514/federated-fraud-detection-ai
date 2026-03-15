import ray # type: ignore
import pandas as pd # type: ignore
import random
from datetime import datetime

@ray.remote
class BankAgent:

    def __init__(self, agent_id, data):
        self.agent_id = agent_id
        self.data = data

    def process_transactions(self):

        events = []

        for _, row in self.data.iterrows():

            event = {
                "agent": self.agent_id,
                "transaction_id": row["transaction_id"],
                "amount": row["amount"],
                "fraud": row["fraud"],
                "timestamp": datetime.now()
            }

            events.append(event)

        return events

    def get_summary(self):

        fraud_count = self.data["fraud"].sum()

        summary = {
            "agent": self.agent_id,
            "transactions": len(self.data),
            "fraud_cases": int(fraud_count)
        }

        return summary