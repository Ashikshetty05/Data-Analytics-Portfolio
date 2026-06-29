import duckdb
import pandas as pd

print("Connecting to DuckDB for Advanced Behavioral Analytics...\n")
conn = duckdb.connect("fintech_ledger.db")

# Advanced Query: Tracking High-Velocity Multi-Trading Behavior
# Uses LAG/LEAD window functions to calculate the time difference between consecutive trades per user
high_velocity_query = """
WITH OrderedTrades AS (
    SELECT 
        user_id,
        broker,
        transaction_type,
        timestamp,
        total_value_inr,
        LEAD(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp) as next_trade_time,
        LEAD(broker) OVER (PARTITION BY user_id ORDER BY timestamp) as next_trade_broker
    FROM platform_transactions
)
SELECT 
    user_id,
    broker as primary_broker,
    next_trade_broker as secondary_broker,
    timestamp as trade_one_time,
    next_trade_time as trade_two_time,
    epoch(next_trade_time) - epoch(timestamp) as time_delta_seconds
FROM OrderedTrades
WHERE next_trade_time IS NOT NULL 
  AND (epoch(next_trade_time) - epoch(timestamp)) <= 3600
LIMIT 5;
"""

print("--- ADVANCED METRIC: DETECTING HIGH-VELOCITY CROSS-BROKER TRADES (<= 60 MINS) ---")
df_velocity = conn.execute(high_velocity_query).df()
print(df_velocity)

conn.close()