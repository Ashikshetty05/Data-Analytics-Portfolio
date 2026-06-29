# Multi-Broker Ledger Warehouse & Behavioral Analytics Pipeline

An enterprise-ready data engineering and portfolio analytics engine designed to consolidate, query, and visualize high-volume transaction logs across prominent Indian brokerage platforms (Zerodha, AngelOne, Groww, Upstox). 
This architecture provisions a local columnar warehouse layer using DuckDB, processes complex transactional logic via native Python transformation vectors, and compiles an executive-level risk telemetry dashboard utilizing decoupled Jinja2 environments.

## 🏗️ System Architecture & Separation of Concerns

The codebase enforces strict separation of infrastructure, transformation, and presentation layers:
1. **Ingestion & Data Provisioning (`pipeline.py`)**: Algorithmic generation engine simulating 10,500 transactional data points across strict operational parameters.
2. **Columnar Storage Layer (`fintech_ledger.db`)**: A localized DuckDB warehouse indexing transaction records using vectorized execution optimizations to enable high-speed historical analytics.
3. **Analytical Processing Layer (`build_dashboard.py`)**: Advanced Python controller that queries data metrics, computes rolling user actions, and handles 100% of formatting logic natively to keep presentation spaces completely decoupled.
4. **Presentation Engine (`template.html` & `dashboard.html`)**: A lightweight HTML interface styled with responsive Tailwind CSS utilities, dynamically populated via a Jinja2 `FileSystemLoader` loop.

---

## 📈 Advanced Analytics: SQL Window Functions

To extract high-value corporate signals, the engine runs advanced analytical window calculations using SQL clauses to detect high-velocity multi-trading behaviors (arbitrage hunting, cross-platform hedging, or slippage exposure) where users execute sequential trades across different broker systems within 60 minutes:

```sql
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

---

## 🚀 Local Installation & Execution

### 1. Environment Setup
```bash
# Navigate to the workspace
cd fintech_analytics

# Activate your isolated local environment path
..\.data_env\Scripts\Activate.ps1

### 2. Run Ingestion Warehouse Compilations
# Generate the DuckDB local warehouse layer (10,500 rows)
python pipeline.py

# Execute the advanced analytic compilation loop
python build_dashboard.py

### 3. Review Local Presentation Layer
# Stream the dynamically compiled dashboard in a local browser tab
Start-Process dashboard.html
