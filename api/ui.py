import streamlit as st
import requests

st.title("🎓 Student Performance Predictor")

# -------------------------------
# Inputs
# -------------------------------
school = st.selectbox("School", ["GP", "MS"])
sex = st.selectbox("Sex", ["M", "F"])
age = st.slider("Age", 15, 22)
studytime = st.slider("Study Time", 1, 4)
failures = st.slider("Failures", 0, 3)
absences = st.slider("Absences", 0, 30)

# -------------------------------
# Prediction via API
# -------------------------------
if st.button("Predict"):

    url = "http://127.0.0.1:8000/predict"

    data = {
        "school": school,
        "sex": sex,
        "age": age,
        "studytime": studytime,
        "failures": failures,
        "absences": absences
    }

    try:
        response = requests.post(url, json=data)

        result = response.json()

        if result["prediction"] == 1:
            st.success("✅ Student will PASS")
        else:
            st.error("❌ Student may FAIL")

    except Exception as e:
        st.error(f"API Error: {e}")