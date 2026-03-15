import flwr as fl # type: ignore
import torch # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore
from model import FraudMLP

from sklearn.preprocessing import LabelEncoder # type: ignore
from sklearn.model_selection import train_test_split # type: ignore


# load dataset
df = pd.read_csv("synthetic_data/transactions.csv")

# encode categorical variables
for col in ["merchant", "location", "device_type", "transaction_type"]:
    df[col] = LabelEncoder().fit_transform(df[col])

df = df.drop(columns=["timestamp"])

X = df.drop("fraud", axis=1).values
y = df["fraud"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

X_train = torch.tensor(X_train).float()
y_train = torch.tensor(y_train).float().view(-1,1)

X_test = torch.tensor(X_test).float()
y_test = torch.tensor(y_test).float().view(-1,1)


model = FraudMLP(X_train.shape[1])

loss_fn = torch.nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


class FlowerClient(fl.client.NumPyClient):

    def get_parameters(self, config):
        return [val.cpu().numpy() for _, val in model.state_dict().items()]

    def set_parameters(self, parameters):

        params_dict = zip(model.state_dict().keys(), parameters)
        state_dict = {k: torch.tensor(v) for k, v in params_dict}
        model.load_state_dict(state_dict)

    def fit(self, parameters, config):

        self.set_parameters(parameters)

        for epoch in range(3):

            optimizer.zero_grad()

            outputs = model(X_train)

            loss = loss_fn(outputs, y_train)

            loss.backward()

            optimizer.step()

        return self.get_parameters(config), len(X_train), {}

    def evaluate(self, parameters, config):

        self.set_parameters(parameters)

        with torch.no_grad():

            outputs = model(X_test)

            loss = loss_fn(outputs, y_test)

            preds = (outputs > 0.5).float()

            accuracy = (preds == y_test).float().mean()

        return float(loss), len(X_test), {"accuracy": float(accuracy)}


fl.client.start_numpy_client(
    server_address="127.0.0.1:8080",
    client=FlowerClient()
)