from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import pandas as pd
import pickle

app = FastAPI()

# Load the model and preprocessing tools
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("encoder.pkl", "rb") as f:
    encoder = pickle.load(f)


# Define input schema
class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.post("/predict")
def predict(data: CustomerData):
    try:
        # Convert to DataFrame
        df = pd.DataFrame([data.dict()])

        # Preprocessing (same order as training!)
        categorical_cols = encoder.feature_names_in_.tolist()
        numerical_cols = scaler.feature_names_in_.tolist()

        df_cat = encoder.transform(df[categorical_cols])
        df_num = scaler.transform(df[numerical_cols])

        X = np.hstack((df_cat, df_num))
        pred = model.predict_proba(X)[0][1]

        return {"churn_probability": pred}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))