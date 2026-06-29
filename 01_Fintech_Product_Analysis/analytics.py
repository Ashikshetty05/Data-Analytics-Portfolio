import duckdb
import pandas as pd

print("Connecting to localized DuckDB analytical warehouse layer...\n")
conn = duckdb.connect("fintech_ledger.db")

# Insight 1: Cross-Broker Market Share Aggregation
print("--- INSIGHT 1: TOTAL CAPITAL VOLUME BY BROKER PLATFORM ---")
query_1 = """
SELECT 
    broker,
    COUNT(transaction_id) as total_trades,
    ROUND(SUM(total_value_inr), 2) as aggregated_volume_inr
FROM platform_transactions
GROUP BY broker
ORDER BY aggregated_volume_inr DESC;
"""
df_broker = conn.execute(query_1).df()
print(df_broker)
print("\n" + "="*60 + "\n")

# Insight 2: High-Frequency Traders (Advanced Window Function)
print("--- INSIGHT 2: RECENT TRANSACTIONS LEDGER PREVIEW (FIRST 10 ROWS) ---")
query_2 = """
SELECT 
    transaction_id,
    timestamp,
    user_id,
    broker,
    transaction_type,
    asset_ticker,
    total_value_inr
FROM platform_transactions
LIMIT 10;
"""
df_preview = conn.execute(query_2).df()
print(df_preview)

conn.close()
print("\nAnalysis engine execution complete.")