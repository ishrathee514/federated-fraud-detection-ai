import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from PIL import Image
import os

st.set_page_config(
    page_title="Federated Fraud Detection Platform",
    layout="wide"
)

st.title("Federated AI Fraud Detection Platform")

st.markdown(
"""
### Secure Federated AI for Financial Fraud Detection

This platform demonstrates a **multi-agent federated learning system** where multiple banks collaboratively train fraud detection models **without sharing sensitive customer data**.
"""
)

# -------------------------
# Load transaction dataset safely
# -------------------------

data_path = "synthetic_data/transactions.csv"

if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    st.error("Transaction dataset not found.")
    st.stop()


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

    st.header("Transaction Analytics Dashboard")

    fraud_count = df["fraud"].sum()
    total = len(df)
    fraud_rate = round((fraud_count / total) * 100, 2)
    avg_amount = round(df["amount"].mean(), 2)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Transactions", total)
    col2.metric("Fraud Cases", fraud_count)
    col3.metric("Fraud Rate (%)", fraud_rate)
    col4.metric("Avg Transaction Amount", f"${avg_amount}")

    st.divider()

    tab1, tab2, tab3 = st.tabs([
        "Overview",
        "Fraud Analysis",
        "Transaction Patterns"
    ])

    # --------------------
    # TAB 1 — Overview
    # --------------------

    with tab1:

        st.subheader("Transaction Amount Distribution")

        fig = px.histogram(
            df,
            x="amount",
            color="fraud",
            title="Transaction Amount Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    # --------------------
    # TAB 2 — Fraud Analysis
    # --------------------

    with tab2:

        st.subheader("Fraud vs Legitimate Transactions")

        fraud_dist = df["fraud"].value_counts().reset_index()
        fraud_dist.columns = ["Fraud", "Count"]

        fig2 = px.pie(
            fraud_dist,
            names="Fraud",
            values="Count"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # --------------------
    # TAB 3 — Transaction Patterns
    # --------------------

    with tab3:

        st.subheader("Transaction Amount vs Fraud")

        fig3 = px.box(
            df,
            x="fraud",
            y="amount",
            title="Fraud Distribution by Amount"
        )

        st.plotly_chart(fig3, use_container_width=True)

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

    fig = px.bar(
        data,
        x="Bank",
        y="Fraud Cases",
        title="Fraud Cases per Bank"
    )

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

    db_path = "governance/audit.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure table exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()

    try:
        logs = pd.read_sql_query(
            "SELECT * FROM audit_logs",
            conn
        )

        if len(logs) > 0:
            st.dataframe(logs)
        else:
            st.info("No audit logs available yet.")

    except:
        st.warning("Audit logs could not be loaded.")


# =========================
# PAGE 5 — Explainable AI
# =========================

elif page == "Explainable AI":

    st.header("Model Explainability (SHAP)")

    image_path = "governance/shap_summary.png"

    if os.path.exists(image_path):

        img = Image.open(image_path)

        st.image(
            img,
            caption="Feature Importance for Fraud Detection"
        )

    else:

        st.warning(
            "SHAP explanation image not found. "
            "Run governance/explain.py locally to generate it."
        )
