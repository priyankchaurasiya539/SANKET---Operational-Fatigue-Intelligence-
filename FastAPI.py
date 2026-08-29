from fastapi import FastAPI
import pandas as pd
import joblib
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI(title="ForceWell AI - Fatigue Risk API")

model = joblib.load('models/rf_model.pkl')
model_columns = joblib.load('models/model_features.pkl')

class JawanData(BaseModel):
    duty_hours: Annotated[float, Field(ge=0.0, le=24.0)]
    sleep_duration: Annotated[float, Field(ge=0.0, le=24.0)]
    temperature_c: Annotated[float, Field(ge=-50.0, le=60.0)]
    service_years: Annotated[int, Field(ge=0, le=45)]
    force_type: str
    role: str
    region: str
    connectivity_status: str
    avg_duty_7d: Annotated[float, Field(ge=0.0, le=24.0)]

@app.post("/predict")
def predict_risk(data: JawanData):
    input_dict = data.dict()
    df_input = pd.DataFrame([input_dict])
    
    categorical_cols = ['force_type', 'role', 'region', 'connectivity_status']
    df_encoded = pd.get_dummies(df_input, columns=categorical_cols)
    df_encoded = df_encoded.reindex(columns=model_columns, fill_value=0)
    
    prediction = model.predict(df_encoded)[0]
    probability = model.predict_proba(df_encoded).max()
    
    # Safety Guardrail Override (Domain Logic for Defense Standards)
    if data.avg_duty_7d > 14.0 or (data.duty_hours > 12 and data.sleep_duration < 5):
        prediction = "HIGH"
        probability = 0.95
    elif data.avg_duty_7d > 11.0 and prediction == "LOW":
        prediction = "MEDIUM"
        probability = 0.80
        
    return {
        "predicted_risk_category": prediction,
        "confidence_score": round(float(probability), 2)
    }