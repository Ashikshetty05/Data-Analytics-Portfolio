import pandas as pd

# The exact file name from your project folder
file_path = "Womens Clothing E-Commerce Reviews.csv"

try:
    # 1. Read the raw CSV file
    df = pd.read_csv(file_path)
    print("\n✅ Dataset successfully loaded into Python memory!")
    print(f"📊 Total Rows: {df.shape[0]} | Total Columns: {df.shape[1]}")
    
    # 2. Print the exact column names for our next data cleaning steps
    print("\n🔍 System Headers Identified:")
    print(df.columns.tolist())
    
except Exception as e:
    print(f"❌ Error reading the dataset: {e}")