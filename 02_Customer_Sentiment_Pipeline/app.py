import streamlit as st
import sqlite3
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="AI Customer Sentiment Dashboard", layout="wide")

st.title("🛍️ E-Commerce Customer Sentiment Analytics")
st.markdown("A live data engineering pipeline analyzing customer feedback using a local **Gemma 2 (2B)** model via Ollama.")
st.markdown("---")

# 2. Database Connection Helper
DB_NAME = "customer_sentiment.db"

def fetch_data(query):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

try:
    # 3. Fetch KPI Summary Metrics
    df_metrics = fetch_data("SELECT AI_Sentiment, COUNT(*) as count FROM sentiment_analysis GROUP BY AI_Sentiment;")
    
    # Map counts to variables for easy UI display
    metrics_dict = dict(zip(df_metrics['AI_Sentiment'], df_metrics['count']))
    pos_count = metrics_dict.get('Positive', 0)
    neg_count = metrics_dict.get('Negative', 0)
    mix_count = metrics_dict.get('Mixed', 0)
    neu_count = metrics_dict.get('Neutral', 0)
    total_reviews = sum(metrics_dict.values())

    # 4. Display KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Reviews Analyzed", total_reviews)
    col2.metric("🟢 Positive Sentiments", pos_count)
    col3.metric("🔴 Negative Sentiments", neg_count)
    col4.metric("🟡 Mixed Sentiments", mix_count)
    col5.metric("⚪ Neutral Sentiments", neu_count)
    
    st.markdown("---")

    # 5. Split layout into Data View and Summary Charts
    left_chart_col, right_table_col = st.columns([1, 1])

    with left_chart_col:
        st.subheader("📊 Sentiment Volume Distribution")
        st.bar_chart(data=df_metrics.set_index('AI_Sentiment'), y='count', color='#4F46E5')

    with right_table_col:
        st.subheader("🔍 Deep Dive: Raw AI Pipeline Output")
        selected_sentiment = st.selectbox("Filter by Sentiment Type:", ["All", "Positive", "Negative", "Mixed", "Neutral"])
        
        if selected_sentiment == "All":
            query_filter = "SELECT Review_Text, Rating, AI_Sentiment, AI_Reason FROM sentiment_analysis;"
        else:
            query_filter = f"SELECT Review_Text, Rating, AI_Sentiment, AI_Reason FROM sentiment_analysis WHERE AI_Sentiment = '{selected_sentiment}';"
            
        df_filtered = fetch_data(query_filter)
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)

except Exception as err:
    st.error(f"Could not connect to the pipeline database: {err}")
    st.info("Ensure you have run 'database_ingestion.py' first to generate your structured tables.")