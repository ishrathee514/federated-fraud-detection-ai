import sqlite3 # type: ignore
import hashlib # type: ignore
from datetime import datetime # type: ignore


DB = "governance/audit.db"


def init_db():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent TEXT,
        event TEXT,
        timestamp TEXT,
        signature TEXT
    )
    """)

    conn.commit()
    conn.close()


def sign_event(agent, event):

    payload = f"{agent}-{event}-{datetime.now()}"

    signature = hashlib.sha256(payload.encode()).hexdigest()

    return signature


def log_event(agent, event):

    signature = sign_event(agent, event)

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO audit_logs (agent, event, timestamp, signature)
    VALUES (?, ?, ?, ?)
    """, (agent, event, str(datetime.now()), signature))

    conn.commit()
    conn.close()


def get_logs():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM audit_logs")

    rows = cursor.fetchall()

    conn.close()

    return rows


if __name__ == "__main__":

    init_db()

    log_event("Bank_A", "transaction_processed")
    log_event("Bank_B", "model_training")
    log_event("Bank_C", "weights_sent")

    logs = get_logs()

    print("\nAudit Logs:\n")

    for row in logs:
        print(row)