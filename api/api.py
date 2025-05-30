from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle

app = FastAPI()

# Load the model and preprocessing tools
with open("/opt/airflow/model/artifacts/model.pkl", "rb") as f:
    model = pickle.load(f)

with open("/opt/airflow/model/artifacts/preprocessor.pkl", "rb") as f:
    preprocessor = pickle.load(f)

with open("/opt/airflow/model/artifacts/selector.pkl", "rb") as f:
    selector = pickle.load(f)


# Define input schema
class CustomerData(BaseModel):
    gender: str
    senior_citizen: int
    partner: str
    dependents: str
    tenure: int
    phone_service: str
    multiple_lines: str
    internet_service: str
    online_security: str
    online_backup: str
    device_protection: str
    tech_support: str
    streaming_tv: str
    streaming_movies: str
    contract: str
    paperless_billing: str
    payment_method: str
    monthly_charges: float
    total_charges: float


def prepare_input(input_data: dict) -> pd.DataFrame:
    df = pd.DataFrame([input_data])

    # Convert numeric fields explicitly
    numeric_cols = ['monthly_charges', 'total_charges', 'tenure', 'senior_citizen']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    # Map senior_citizen from 0/1 to 'No'/'Yes'
    df['senior_citizen'] = df['senior_citizen'].map({0: 'No', 1: 'Yes'})

    # Replace training-specific strings
    df.replace({
        'No phone service': 'No',
        'No internet service': 'No'
    }, inplace=True)

    return df


@app.post("/predict")
def predict(data: CustomerData):
    try:
        # Prepare input data
        input_df = prepare_input(data.dict())

        # Apply preprocessing
        X_preprocessed = preprocessor.transform(input_df)

        # Feature selection
        X_selected = selector.transform(X_preprocessed)

        # Predict churn probability
        prob_churn = model.predict_proba(X_selected)[0][1]

        return {"churn_probability": round(float(prob_churn), 4)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))