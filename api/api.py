from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import os

app = FastAPI()

# -------------------------------
# Load Model + Columns
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = pickle.load(open(os.path.join(BASE_DIR, "model/model.pkl"), "rb"))
columns = pickle.load(open(os.path.join(BASE_DIR, "model/columns.pkl"), "rb"))

# -------------------------------
# Define Input Schema
# -------------------------------
class Student(BaseModel):
    school: str
    sex: str
    age: int
    studytime: int
    failures: int
    absences: int

# -------------------------------
# Routes
# -------------------------------
@app.get("/")
def home():
    return {"message": "API Running"}

@app.post("/predict")
def predict(data: Student):

    # Convert to DataFrame
    input_df = pd.DataFrame([data.dict()])

    # Encoding
    input_encoded = pd.get_dummies(input_df)

    # Add missing columns
    for col in columns:
        if col not in input_encoded:
            input_encoded[col] = 0

    input_encoded = input_encoded[columns]

    # Prediction
    prediction = model.predict(input_encoded)

    return {
        "prediction": int(prediction[0]),
        "result": "Pass" if prediction[0] == 1 else "Fail"
    }