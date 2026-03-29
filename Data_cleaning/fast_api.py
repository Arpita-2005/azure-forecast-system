from fastapi import FastAPI
import pandas as pd
import joblib
import json

app = FastAPI()

model = joblib.load("models/final_xgboost_model.pkl")

with open("models/model_columns.json") as f:
    columns = json.load(f)

@app.get("/")
def home():
    return {"message": "API running"}

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    df = df.reindex(columns=columns, fill_value=0)
    pred = model.predict(df)
    return {"prediction": float(pred[0])}
