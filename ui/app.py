import streamlit as st # type: ignore 
import pandas as pd # type: ignore 
import sqlite3
import plotly.express as px # type: ignore 
from PIL import Image # type: ignore 


st.set_page_config(page_title="Federated Fraud Detection Platform",layout="wide")


st.title("Federated AI Fraud Detection Platform")


# -------------------------
# Load transaction dataset
# -------------------------

df = pd.read_csv("synthetic_data/transactions.csv")


# -------------------------
# Sidebar Navigation
# -------------------------

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Transaction Analytics",
        "Agent Activity",
        "Federated Learning",
        "Governance Logs",
        "Explainable AI"
    ]
)


# =========================
# PAGE 1 — Transaction Analytics
# =========================

if page == "Transaction Analytics":

    st.header("Transaction Analytics")

    fraud_count = df["fraud"].sum()
    total = len(df)

    col1, col2 = st.columns(2)

    col1.metric("Total Transactions", total)
    col2.metric("Fraud Cases", fraud_count)

    fig = px.histogram(df, x="amount", color="fraud",title="Transaction Amount Distribution")

    st.plotly_chart(fig)


# =========================
# PAGE 2 — Agent Activity
# =========================

elif page == "Agent Activity":

    st.header("Bank Agent Activity")

    bank_A = df.iloc[:1600]
    bank_B = df.iloc[1600:3200]
    bank_C = df.iloc[3200:]

    data = pd.DataFrame({

        "Bank": ["Bank_A", "Bank_B", "Bank_C"],

        "Transactions": [
            len(bank_A),
            len(bank_B),
            len(bank_C)
        ],

        "Fraud Cases": [
            bank_A["fraud"].sum(),
            bank_B["fraud"].sum(),
            bank_C["fraud"].sum()
        ]
    })

    st.dataframe(data)

    fig = px.bar(data,
                 x="Bank",
                 y="Fraud Cases",
                 title="Fraud Cases per Bank")

    st.plotly_chart(fig)


# =========================
# PAGE 3 — Federated Learning
# =========================

elif page == "Federated Learning":

    st.header("Federated Learning Status")

    st.write("""
    Federated learning allows multiple banks to train a shared fraud detection model 
    without sharing raw customer data.
    """)

    st.success("Model training completed successfully across agents")


# =========================
# PAGE 4 — Governance Logs
# =========================

elif page == "Governance Logs":

    st.header("Audit Logs")

    conn = sqlite3.connect("governance/audit.db")

    logs = pd.read_sql_query(
        "SELECT * FROM audit_logs",
        conn
    )

    st.dataframe(logs)


# =========================
# PAGE 5 — Explainable AI
# =========================

elif page == "Explainable AI":

    st.header("Model Explainability (SHAP)")

    img = Image.open("governance/shap_summary.png")

    st.image(img, caption="Feature Importance for Fraud Detection")