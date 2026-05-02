import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load cleaned data
df = pd.read_csv("data/cleaned_data.csv")

print("Loaded cleaned data...")
print(df.head())

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

# Function to classify sentiment
def get_sentiment(text):
    score = analyzer.polarity_scores(str(text))['compound']
    
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"

# Apply sentiment analysis
df['sentiment'] = df['clean_text'].apply(get_sentiment)

# Save final dataset
df.to_csv("data/final_output.csv", index=False)

print("Sentiment analysis completed and saved!")
print(df['sentiment'].value_counts())