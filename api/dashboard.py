import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Sentiment Dashboard", layout="wide")

st.title("📊 Social Media Sentiment Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    try:
        url = "http://127.0.0.1:8001/data"
        response = requests.get(url, timeout=5)
        data = response.json()
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data available")
    st.stop()

# 🔹 Sidebar Filters
st.sidebar.header("🔍 Filters")

platform = st.sidebar.multiselect(
    "Select Platform",
    options=df['platform'].unique(),
    default=df['platform'].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['date'].min(), df['date'].max()]
)

# Apply filters
filtered_df = df[
    (df['platform'].isin(platform)) &
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1]))
]

# 🔹 KPI SECTION
st.subheader("📌 Key Insights")

col1, col2, col3, col4 = st.columns(4)

total = len(filtered_df)
positive = len(filtered_df[filtered_df['sentiment'] == "Positive"])
negative = len(filtered_df[filtered_df['sentiment'] == "Negative"])
neutral = len(filtered_df[filtered_df['sentiment'] == "Neutral"])

col1.metric("Total Posts", total)
col2.metric("Positive", positive)
col3.metric("Negative", negative)
col4.metric("Neutral", neutral)

# 🔹 Charts Layout
colA, colB = st.columns(2)

# Pie Chart
with colA:
    fig1 = px.pie(filtered_df, names='sentiment', title='Sentiment Distribution')
    st.plotly_chart(fig1, use_container_width=True)

# Bar Chart
with colB:
    fig2 = px.histogram(filtered_df, x='platform', color='sentiment', barmode='group')
    st.plotly_chart(fig2, use_container_width=True)

    from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.subheader("🔤 Word Cloud")

text = " ".join(filtered_df['clean_text'].dropna().astype(str))

if text.strip():
    wc = WordCloud(width=800, height=400, background_color='black').generate(text)

    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')

    st.pyplot(fig)
else:
    st.warning("No text available for word cloud")
    st.subheader("🧠 Live Sentiment Prediction")

user_input = st.text_input("Enter text to analyze")

def simple_sentiment(text):
    text = text.lower()
    if "good" in text or "great" in text or "fantastic" in text:
        return "Positive 😊"
    elif "bad" in text or "worst" in text:
        return "Negative 😡"
    else:
        return "Neutral 😐"

if user_input:
    result = simple_sentiment(user_input)
    st.success(f"Predicted Sentiment: {result}")

# 🔹 Trend
st.subheader("📈 Sentiment Trend")

trend = filtered_df.groupby(['date', 'sentiment']).size().reset_index(name='count')

fig3 = px.line(trend, x='date', y='count', color='sentiment')
st.plotly_chart(fig3, use_container_width=True)

# 🔹 Data Table
st.subheader("📄 Raw Data")
st.dataframe(filtered_df)
st.subheader("🚨 Sentiment Alerts")

daily = filtered_df.groupby('date').size()

if len(daily) > 1:
    if daily.iloc[-1] > daily.mean() * 1.5:
        st.error("⚠️ Spike detected in activity!")
    else:
        st.success("No unusual activity detected")
        st.subheader("📥 Download Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="sentiment_data.csv",
    mime="text/csv"
)