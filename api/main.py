from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import numpy as np
import shap
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.schemas import PatientInput, PredictionOutput

app = FastAPI(title='Alzheimer Detection API', version='1.0')

app.add_middleware(CORSMiddleware,
    allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

model         = joblib.load('models/xgboost_final.pkl')
scaler        = joblib.load('models/scaler.pkl')
feature_names = joblib.load('models/feature_names.pkl')

# Features continues : normalisées par StandardScaler
# Les features binaires (Smoking, FamilyHistory…) sont exclues intentionnellement

CONTINUOUS = ['Age', 'BMI', 'AlcoholConsumption', 'PhysicalActivity',
              'DietQuality', 'SleepQuality', 'SystolicBP', 'DiastolicBP',
              'CholesterolTotal', 'CholesterolLDL', 'CholesterolHDL',
              'CholesterolTriglycerides', 'MMSE', 'FunctionalAssessment', 'ADL']

def severity(proba):
    # Seuils alignés sur les pratiques de screening clinique Alzheimer
    if proba < 0.3:  return 'Risque faible'
    if proba < 0.6:  return 'Risque modéré'
    return 'Risque élevé'

def get_prediction(patient_dict):
    df = pd.DataFrame([patient_dict])
     #  compléter les features manquantes avec 0

    for col in feature_names:
        if col not in df.columns:
            df[col] = 0
    df = df[feature_names]

    # Normalisation des features continues uniquement

    cont = [c for c in CONTINUOUS if c in df.columns]
    df[cont] = scaler.transform(df[cont])
    proba      = float(model.predict_proba(df)[0, 1])
    prediction = 'Alzheimer' if proba >= 0.5 else 'Non-Alzheimer'


    explainer  = shap.TreeExplainer(model)
    shap_vals  = explainer.shap_values(df)[0]

     # Top 5 features par impact absolu
    top5 = sorted(zip(feature_names, shap_vals),
                  key=lambda x: abs(x[1]), reverse=True)[:5]
    return proba, prediction, top5, df

@app.get('/health')
def health():
    return {'status': 'ok', 'model': 'xgboost_final'}

@app.post('/predict', response_model=PredictionOutput)
def predict(patient: PatientInput):
    try:
        proba, prediction, top5, df = get_prediction(patient.dict())
        return {
            'risk_score'  : round(proba, 4),
            'prediction'  : prediction,
            'severity'    : severity(proba),
            'top_factors' : [{'feature': f, 'impact': round(float(v), 4)} for f, v in top5],
            'alert'       : proba > 0.7
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/predict/fhir')
def predict_fhir(patient: PatientInput):
    try:
        proba, prediction, top5, df = get_prediction(patient.dict())
        return {
            "resourceType": "Observation",
            "status": "final",
            "code": {
                "coding": [{
                    "system": "http://loinc.org",
                    "code": "72166-2",
                    "display": "Alzheimer Disease Risk Assessment"
                }]
            },
            "valueQuantity": {
                "value": round(proba, 4),
                "unit": "probability",
                "system": "http://unitsofmeasure.org"
            },
            "interpretation": [{
                "coding": [{
                    "system": "http://hl7.org/fhir/v2/0078",
                    "code": "H" if proba > 0.7 else "I" if proba > 0.3 else "N",
                    "display": severity(proba)
                }]
            }],
            "component": [
                {
                    "code": {"text": f},
                    "valueQuantity": {"value": round(float(v), 4)}
                }
                for f, v in top5
            ],
            "note": [{
                "text": f"Prédiction : {prediction}. Score : {round(proba*100, 1)}%. "
                        f"Alerte : {'Oui' if proba > 0.7 else 'Non'}"
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
