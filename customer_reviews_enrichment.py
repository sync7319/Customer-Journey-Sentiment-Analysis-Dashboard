"""
This script pulls customer reviews from SQL Server, runs sentiment 
analysis with VADER, combines sentiment scores with review ratings 
to classify reviews, and saves the results to CSV. The output includes 
a sentiment score, a sentiment category, and a bucketed score range 
for easier reporting and aggregation.
"""

import pandas as pd
import pyodbc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure VADER lexicon available
nltk.download('vader_lexicon')

def fetch_data_from_sql():
    """Fetch customer reviews from SQL Server."""
    conn_str = (
        "Driver={SQL Server};"
        "Server=Gaming-PC\\SQLEXPRESS;"
        "Database=PortfolioProject_MarketingAnalytics;"
        "Trusted_Connection=yes;"
    )
    conn = pyodbc.connect(conn_str)
    query = """
        SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText 
        FROM dbo.fact_customer_reviews
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

print("ATTEMPT CHECKPOINT 1")
customer_reviews_df = fetch_data_from_sql()
print("REACHED CHECKPOINT 1")

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

def calculate_sentiment(review):
    """Return compound sentiment score (-1 to 1)."""
    return sia.polarity_scores(review)['compound']

def categorize_sentiment(score, rating):
    """Combine sentiment score and rating into a sentiment category."""
    if score > 0.05:
        if rating >= 4: return 'Positive'
        elif rating == 3: return 'Mixed Positive'
        else: return 'Mixed Negative'
    elif score < -0.05:
        if rating <= 2: return 'Negative'
        elif rating == 3: return 'Mixed Negative'
        else: return 'Mixed Positive'
    else:
        if rating >= 4: return 'Positive'
        elif rating <= 2: return 'Negative'
        else: return 'Neutral'

def sentiment_bucket(score):
    """Bucket sentiment score into ranges."""
    if score >= 0.5: return '0.5 to 1.0'
    elif score >= 0.0: return '0.0 to 0.49'
    elif score >= -0.5: return '-0.49 to 0.0'
    else: return '-1.0 to -0.5'

# Apply sentiment analysis
customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)
customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis=1)
customer_reviews_df['SentimentBucket'] = customer_reviews_df['SentimentScore'].apply(sentiment_bucket)

# Preview results
print(customer_reviews_df.head())

# Save results
customer_reviews_df.to_csv(
    r'C:\Users\omarv\OneDrive\Desktop\Portofolio\Solving A Business Problem (Python, SQL, PowerBI)\fact_customer_reviews_with_sentiment.csv', 
    index=False
)