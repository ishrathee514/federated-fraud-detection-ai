import shap # type: ignore
import pandas as pd # type: ignore 
import matplotlib.pyplot as plt # type: ignore 

from sklearn.ensemble import RandomForestClassifier # type: ignore
from sklearn.preprocessing import LabelEncoder # type: ignore


# load dataset
df = pd.read_csv("synthetic_data/transactions.csv")

# drop timestamp
df = df.drop(columns=["timestamp"])

# encode categorical columns
categorical_cols = ["merchant", "location", "device_type", "transaction_type"]

for col in categorical_cols:
    df[col] = LabelEncoder().fit_transform(df[col])

# split features and target
X = df.drop("fraud", axis=1)
y = df["fraud"]

# train model
model = RandomForestClassifier()
model.fit(X, y)

# SHAP explanation
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# generate SHAP plot
shap.summary_plot(shap_values, X, show=False)

plt.savefig("governance/shap_summary.png")

print("SHAP explanation saved successfully")