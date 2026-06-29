import pandas as pd
import numpy as np
import random
import duckdb
from datetime import datetime, timedelta

print("Initializing mock fintech ledger generation engine...")

# Ensure data is randomized yet replicable for testing
np.random.seed(42)
random.seed(42)
num_records = 10500

# Step A: Structural Array Definitions (Indian Fintech Ecosystem)
user_ids = [f"USER_{1000 + i}" for i in range(150)]
brokers = ["Zerodha", "Groww", "Upstox", "AngelOne"]
tx_types = ["BUY", "SELL", "DIVIDEND", "DEPOSIT", "WITHDRAWAL"]
assets = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "TATAMOTORS", "ZOMATO"]

# Step B: Set up dates and categorical lists sequentially matching num_records
start_date = datetime(2026, 1, 1)
date_list = [start_date + timedelta(minutes=int(i * 45)) for i in range(num_records)]
chosen_tx_types = [random.choice(tx_types) for _ in range(num_records)]

data = {
    "transaction_id": [f"TXN_{100000 + i}" for i in range(num_records)],
    "timestamp": date_list,
    "user_id": [random.choice(user_ids) for _ in range(num_records)],
    "broker": [random.choice(brokers) for _ in range(num_records)],
    "transaction_type": chosen_tx_types,
    "asset_ticker": [random.choice(assets) if t in ["BUY", "SELL", "DIVIDEND"] else "INR_CASH" for t in chosen_tx_types],
    "volume": np.round(np.random.uniform(1.0, 500.0, num_records), 2),
    "unit_price_inr": np.round(np.random.uniform(10.0, 3500.0, num_records), 2),
    "platform_fee_inr": np.round(np.random.uniform(2.0, 20.0, num_records), 2)
}

# Step C: Compile DataFrame and calculate derived column values
df = pd.DataFrame(data)
df["total_value_inr"] = np.where(
    df["asset_ticker"] == "INR_CASH",
    df["volume"],
    np.round((df["volume"] * df["unit_price_inr"]) + df["platform_fee_inr"], 2)
)

# Step D: Stream data directly into a local analytical DuckDB file
print("Writing rows directly to local persistent DuckDB warehouse layer...")
conn = duckdb.connect("fintech_ledger.db")
conn.execute("CREATE OR REPLACE TABLE platform_transactions AS SELECT * FROM df")
conn.close()

print(f"Success! Managed database file built. 10,500 transaction logs securely indexed.")