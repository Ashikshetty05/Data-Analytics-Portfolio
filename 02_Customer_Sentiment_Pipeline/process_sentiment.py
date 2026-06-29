import pandas as pd
import ollama
import time

# 1. Pipeline Configurations
INPUT_FILE = "cleaned_reviews_sample.csv"
OUTPUT_FILE = "ai_analyzed_reviews_sample.csv"
MODEL_NAME = "gemma2:2b"

print(f"🤖 Loading dataset and initializing local AI Engine ({MODEL_NAME})...")

try:
    # 2. Ingest the 100-row cleaned sample data
    df = pd.read_csv(INPUT_FILE)
    
    # Initialize empty tracking lists for our target metrics
    sentiments = []
    reasons = []
    
    start_time = time.time()
    
    # 3. Stream data through the local engine row-by-row
    for index, row in df.iterrows():
        review_text = row['Review Text']
        rating = row['Rating']
        
        # Build a strict operational prompt optimized for Gemma 2
        prompt = f"""
        You are a strict data validation assistant. Analyze this e-commerce customer review:
        Review: "{review_text}"
        Customer Rating: {rating} stars out of 5.
        
        Provide your analysis in exactly two short sentences:
        Sentence 1: Start with 'Sentiment: ' followed by exactly one word (Positive, Negative, or Neutral).
        Sentence 2: Start with 'Reason: ' followed by a brief, single-sentence summary explaining why.
        """
        
        try:
            # Send prompt to your completely private local hardware layer
            response = ollama.generate(model=MODEL_NAME, prompt=prompt)
            output_text = response['response'].strip()
            
            # Parse out the data lines cleanly
            lines = output_text.split('\n')
            sentiment = "Neutral"
            reason = "Analysis complete."
            
            for line in lines:
                if line.startswith("Sentiment:"):
                    sentiment = line.replace("Sentiment:", "").strip()
                elif line.startswith("Reason:"):
                    reason = line.replace("Reason:", "").strip()
            
            sentiments.append(sentiment)
            reasons.append(reason)
            print(f"✅ Processed Row {index + 1}/100 | Sentiment Caught: {sentiment}")
            
        except Exception as ai_err:
            print(f"⚠️ Row {index + 1} Processing Error: {ai_err}")
            sentiments.append("Error")
            reasons.append("AI framework timeout.")
            
    # 4. Integrate data insights back into the core Dataframe
    df['AI_Sentiment'] = sentiments
    df['AI_Reason'] = reasons
    
    # 5. Export structural dataset back to disk
    df.to_csv(OUTPUT_FILE, index=False)
    
    end_time = time.time()
    duration = end_time - start_time
    print(f"\n🎉 Pipeline Complete! Output generated at '{OUTPUT_FILE}' in {duration:.2f} seconds.")
    
except Exception as e:
    print(f"❌ Critical Pipeline Failure: {e}")