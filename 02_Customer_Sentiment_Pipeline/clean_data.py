import pandas as pd

# 1. Load the raw dataset
raw_file = "Womens Clothing E-Commerce Reviews.csv"
output_file = "cleaned_reviews_sample.csv"

try:
    df = pd.read_csv(raw_file)
    print("✨ Step 1: Raw data loaded successfully.")
    
    # 2. Select only the business-critical columns we need
    keep_columns = ['Clothing ID', 'Age', 'Review Text', 'Rating', 'Department Name']
    df_filtered = df[keep_columns].copy()
    
    # 3. Handle Missing Data: Drop rows where 'Review Text' or 'Department Name' is blank
    df_filtered = df_filtered.dropna(subset=['Review Text', 'Department Name'])
    print(f"✨ Step 2: Removed missing records. Rows remaining: {len(df_filtered)}")
    
    # 4. Take a clean, randomized sample of 100 records for our AI Prototype
    df_sample = df_filtered.sample(n=100, random_state=42).copy()
    
    # 5. Export to a clean CSV file
    df_sample.to_csv(output_file, index=False)
    print(f"✅ Step 3: Successfully exported 100 high-quality test rows to '{output_file}'!")
    
except Exception as e:
    print(f"❌ Error during data cleaning phase: {e}")