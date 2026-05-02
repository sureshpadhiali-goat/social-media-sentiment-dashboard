import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Download stopwords (only first time)
nltk.download('stopwords')

# Load dataset
df = pd.read_csv("data/raw_data.csv")

print("Original Data:")
print(df.head())

# Initialize stopwords
stop_words = set(stopwords.words('english'))

# Cleaning function
def clean_text(text):
    text = str(text).lower()  # lowercase
    
    text = re.sub(r"http\S+", "", text)  # remove URLs
    text = re.sub(r"[^a-zA-Z ]", "", text)  # remove special characters
    
    words = text.split()
    
    words = [word for word in words if word not in stop_words]  # remove stopwords
    
    return " ".join(words)

# Apply cleaning
df['clean_text'] = df['content'].apply(clean_text)

# Save cleaned data
df.to_csv("data/cleaned_data.csv", index=False)

print("Cleaned Data Saved Successfully!")