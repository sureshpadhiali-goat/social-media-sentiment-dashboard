import pandas as pd
import random
from datetime import datetime, timedelta

platforms = ["Twitter", "Instagram", "Reddit"]

positive_texts = [
    "I love this product!",
    "Amazing experience, highly recommend",
    "Best service ever",
    "Super happy with the quality",
    "Absolutely fantastic!"
]

negative_texts = [
    "Worst experience ever",
    "Very disappointed with the service",
    "Not worth the money",
    "Terrible quality",
    "I hate this product"
]

neutral_texts = [
    "It's okay, nothing special",
    "Average experience",
    "Not bad, not great",
    "Could be better",
    "Decent overall"
]

def generate_post():
    sentiment_type = random.choice(["positive", "negative", "neutral"])
    
    if sentiment_type == "positive":
        text = random.choice(positive_texts)
    elif sentiment_type == "negative":
        text = random.choice(negative_texts)
    else:
        text = random.choice(neutral_texts)

    return text

data = []

start_date = datetime(2026, 1, 1)

for i in range(500):
    date = start_date + timedelta(days=random.randint(0, 120))
    
    data.append({
        "id": i,
        "date": date.strftime("%Y-%m-%d"),
        "platform": random.choice(platforms),
        "user": f"user_{random.randint(1,100)}",
        "content": generate_post()
    })

df = pd.DataFrame(data)

df.to_csv("data/raw_data.csv", index=False)

print("Dataset generated successfully!")