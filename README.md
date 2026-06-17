# Détection Précoce de la Maladie d'Alzheimer

Système de scoring basé sur XGBoost et données cliniques structurées.

## Équipe
- Rayane BOUKHERROUF
- Mikhael Le Merveilleux BOUITY
- Brahim Sidi ISSAKHA ADOUM
- Joan Steeve EDANDE OTYE

## Résultats
- Précision : 96%
- Recall Alzheimer : 94%
- AUC-ROC : 0.94

## Installation
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement
```bash
# API
uvicorn api.main:app --reload --port 8000

# Interface
streamlit run frontend/app.py
```

## Stack technique
- XGBoost, SHAP, scikit-learn, FastAPI, Streamlit