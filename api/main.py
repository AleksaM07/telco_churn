import os
import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

env_path = '.env'
if os.path.exists(env_path):
    from dotenv import load_dotenv
    load_dotenv(env_path)

# Load artifacts
model = joblib.load(os.getenv('MODEL_PATH'))
columns = pd.read_parquet(os.getenv('PARQUET_PATH')).drop(columns=['customerID', 'churn'])
cols = list(pd.get_dummies(columns).columns)

app = FastAPI()

class Customer(BaseModel):
    data: dict

@app.post('/predict')
async def predict(customer: Customer):
    df = pd.DataFrame([customer.data])
    try:
        df_enc = pd.get_dummies(df)
        for c in cols:
            if c not in df_enc:
                df_enc[c] = 0
        df_enc = df_enc[cols]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    prob = model.predict_proba(df_enc)[:,1][0]
    return {'churn_probability': float(prob)}