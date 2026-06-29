import duckdb
from jinja2 import Environment, FileSystemLoader

print("Connecting to local DuckDB Warehouse Layer...")
conn = duckdb.connect("fintech_ledger.db")

# 1. Fetch Aggregated Data Summary Metrics
stats = conn.execute("""
    SELECT COUNT(*), ROUND(SUM(total_value_inr), 2), COUNT(DISTINCT user_id)
    FROM platform_transactions
""").fetchone()

total_trades = f"{stats[0]:,}"
total_volume = f"₹{stats[1]:,}"
active_users = f"{stats[2]:,}"

# 2. Fetch and Format Broker Rankings 
raw_brokers = conn.execute("""
    SELECT broker, COUNT(*), ROUND(SUM(total_value_inr)/10000000, 2)
    FROM platform_transactions
    GROUP BY broker
    ORDER BY SUM(total_value_inr) DESC
""").fetchall()
formatted_brokers = [(b, f"{c:,}", f"₹{v:,.2f} Cr") for b, c, v in raw_brokers]

# 3. NEW: Fetch Advanced Behavioral Signals (Window Functions)
high_velocity_query = """
WITH OrderedTrades AS (
    SELECT 
        user_id, broker, timestamp,
        LEAD(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp) as next_trade_time,
        LEAD(broker) OVER (PARTITION BY user_id ORDER BY timestamp) as next_trade_broker
    FROM platform_transactions
)
SELECT 
    user_id, broker, next_trade_broker, timestamp, next_trade_time,
    epoch(next_trade_time) - epoch(timestamp) as time_delta_seconds
FROM OrderedTrades
WHERE next_trade_time IS NOT NULL 
  AND (epoch(next_trade_time) - epoch(timestamp)) <= 3600
LIMIT 5;
"""
raw_velocity = conn.execute(high_velocity_query).fetchall()

formatted_velocity = []
for u_id, p_b, s_b, t1, t2, delta in raw_velocity:
    clean_t1 = t1.strftime("%Y-%m-%d %H:%M:%S")
    clean_t2 = t2.strftime("%Y-%m-%d %H:%M:%S")
    mins_delta = f"{int(delta // 60)} minutes"
    formatted_velocity.append((u_id, p_b, s_b, clean_t1, clean_t2, mins_delta))

# 4. Fetch Recent Standard Transactions 
raw_ledger = conn.execute("""
    SELECT transaction_id, timestamp, user_id, broker, transaction_type, asset_ticker, total_value_inr
    FROM platform_transactions
    LIMIT 8
""").fetchall()

formatted_ledger = []
for tx_id, ts, u_id, broker, tx_type, asset, val in raw_ledger:
    clean_ts = ts.strftime("%Y-%m-%d %H:%M:%S") 
    clean_val = f"₹{val:,.2f}"                  
    formatted_ledger.append((tx_id, clean_ts, u_id, broker, tx_type, asset, clean_val))

conn.close()

# 5. Compile Everything with Jinja2 Loader
print("Compiling production dashboard with advanced telemetry matrix...")
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("template.html")

rendered_html = template.render(
    total_volume=total_volume,
    total_trades=total_trades,
    active_users=active_users,
    broker_data=formatted_brokers,
    velocity_rows=formatted_velocity,
    ledger_rows=formatted_ledger
)

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(rendered_html)

print("Success! Complex data model compiled cleanly into dashboard.html.")