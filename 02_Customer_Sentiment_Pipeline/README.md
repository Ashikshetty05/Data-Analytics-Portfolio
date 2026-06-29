# Local AI E-Commerce Customer Sentiment Data Pipeline

## 📌 Project Overview
This project is an end-to-end, data engineering and AI pipeline designed to ingest unstructured e-commerce customer reviews, execute automated data cleaning, process the text through a completely offline, local Large Language Model (LLM) to extract sentiment analysis, and serve the structured insights via a live relational database and interactive web analytics dashboard.

By deploying the LLM locally, this architecture ensures **100% data privacy** and eliminates cloud API transaction fees, making it an ideal blueprint for enterprise data processing handling sensitive customer information.

## 🛠️ Tech Stack & Core Architecture
* **Data Processing Layer:** Python, Pandas, NumPy
* **AI Processing Engine:** Ollama Framework
* **Local LLM Model:** Google Gemma 2 (2B Parameters, Optimized FP16 quantized)
* **Storage Layer:** Relational SQLite Database Engine
* **Frontend Analytics Interface:** Streamlit Framework
* **Development Environment:** Python Virtual Environments (`venv`), Windows PowerShell

---

## 🔄 Architectural Workflow & Data Flow
1. **Ingestion & Data Cleansing (`clean_data.py`):** Ingests raw historical e-commerce customer feedback records, validates structural integrity, removes null/missing review text, and isolates a randomized 100-row test dataset (`cleaned_reviews_sample.csv`) for local AI optimization.
2. **Local AI Inference Engine (`process_sentiment.py`):**
   Streams the unstructured text data row-by-row into the local Gemma 2 engine running via Ollama. It enforces structural prompts ensuring the model outputs a strict category (`Positive`, `Negative`, `Neutral`, or `Mixed`) along with a qualitative engineering reason string.
3. **Structured Relational Storage (`database_ingestion.py`):**
   Converts the updated text dataset into relational database tables inside a local SQLite database file (`customer_sentiment.db`). It automatically applies database schema standards, normalizes column names, and executes validation checks.
4. **Interactive BI Dashboard (`app.py`):**
   A live web application built in Python that queries the SQLite database dynamically. It calculates high-level KPI card metrics, maps out volume distributions via native charts, and includes an interactive filtration matrix for raw data auditing.

---

## ⚡ Real-World Pipeline Performance Metrics
* **Total Volume Processed:** 100 customer feedback transactions
* **Hardware Compute Layer:** Local AMD Ryzen 5 CPU (16 GB RAM System Allocation)
* **Total Pipeline Execution Duration:** **540.74 seconds** (~5.4 seconds per transaction)
* **AI Model Nuance Accuracy:** Captured sophisticated `Mixed` sentiment metrics (7 total records) where star ratings conflicted with user review descriptions.
* **Operating Cost:** $0.00 (Completely open-source, offline processing)

---

## 📂 File Structure Directory
```text
02_Customer_Sentiment_Pipeline/
├── app.py                         # Streamlit UI Analytics Dashboard
├── clean_data.py                  # Pandas Data Cleansing Ingestion Layer
├── database_ingestion.py          # SQLite Relational Storage Connection Script
├── process_sentiment.py           # Local Ollama/Gemma 2 Inference Engine Script
├── customer_sentiment.db          # Live Local SQLite Relational Database 
├── cleaned_reviews_sample.csv      # Cleaned Data Sample File (Pre-AI)
├── ai_analyzed_reviews_sample.csv # Final AI Output Dataset Asset (Post-AI)
└── README.md                      # Production Documentation

## 🚀 How to Run the System Locally

### Step 1.**Initialize the Local AI Model Environment:**
   ```powershell
   ollama run gemma2:2b

### Step 2. **Execute the End-to-End Code Sequence:**
  ```powershell
  python clean_data.py
  python process_sentiment.py
  python database_ingestion.py

### Step 3. **Launch the Live Interface:**
  ```powershell
  streamlit run app.py