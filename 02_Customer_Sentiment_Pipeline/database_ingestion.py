import pandas as pd
import sqlite3

# 1. Configuration Constants
INPUT_FILE = "ai_analyzed_reviews_sample.csv"
DB_NAME = "customer_sentiment.db"
TABLE_NAME = "sentiment_analysis"

print("🗄️ Initializing SQL Ingestion Layer...")

try:
    # 2. Read the AI-generated CSV file
    df = pd.read_csv(INPUT_FILE)
    print(f"📋 Step 1: Loaded {len(df)} rows from AI output file.")
    
    # 3. Clean up column names for relational database standards (replace spaces with underscores)
    df.columns = df.columns.str.replace(' ', '_')
    
    # 4. Establish Connection to SQLite Database (will create the file if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    
    # 5. Load the DataFrame straight into an optimized SQL table
    # if_exists='replace' ensures that if we re-run the script, it refreshes cleanly
    df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
    print(f"✅ Step 2: Successfully created table '{TABLE_NAME}' in database '{DB_NAME}'.")
    
    # 6. Verify the data injection by running a test query
    print("🔍 Step 3: Running internal verification query...")
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*), AI_Sentiment FROM {TABLE_NAME} GROUP BY AI_Sentiment;")
    summary_results = cursor.fetchall()
    
    print("\n--- Current Data Distribution in SQL ---")
    for row in summary_results:
        print(f"Sentiment: {row[1]} | Count: {row[0]}")
    print("----------------------------------------\n")
    
    # Close out the connection safely
    conn.close()
    print("🎉 Database ingestion process complete! Connection closed.")

except Exception as e:
    print(f"❌ Critical Database Ingestion Failure: {e}")