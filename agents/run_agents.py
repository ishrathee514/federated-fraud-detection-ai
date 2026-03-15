import ray # type: ignore
import pandas as pd # type: ignore
from agent import BankAgent

ray.init()

# load dataset
df = pd.read_csv("synthetic_data/transactions.csv")

# split dataset between banks
split1 = df.sample(frac=0.33, random_state=42)
remaining = df.drop(split1.index)

split2 = remaining.sample(frac=0.5, random_state=42)
split3 = remaining.drop(split2.index)

# create agents
bank_A = BankAgent.remote("Bank_A", split1)
bank_B = BankAgent.remote("Bank_B", split2)
bank_C = BankAgent.remote("Bank_C", split3)

# process transactions
events = ray.get([
    bank_A.process_transactions.remote(),
    bank_B.process_transactions.remote(),
    bank_C.process_transactions.remote()
])

# get summaries
summaries = ray.get([
    bank_A.get_summary.remote(),
    bank_B.get_summary.remote(),
    bank_C.get_summary.remote()
])

print("\nAgent summaries:\n")

for s in summaries:
    print(s)