from pydantic import BaseModel, Field
from typing import List, Optional

class PatientInput(BaseModel):
    # Scores cognitifs
    MMSE               : float = Field(..., ge=0, le=30)
    FunctionalAssessment: float = Field(..., ge=0, le=10)
    ADL                : float = Field(..., ge=0, le=10)
    # Symptômes
    MemoryComplaints   : int   = Field(..., ge=0, le=1)
    BehavioralProblems : int   = Field(..., ge=0, le=1)
    Confusion          : int   = Field(..., ge=0, le=1)
    Disorientation     : int   = Field(..., ge=0, le=1)
    PersonalityChanges : int   = Field(..., ge=0, le=1)
    Forgetfulness      : int   = Field(..., ge=0, le=1)
    # Démographie
    Age                : float = Field(..., ge=60, le=90)
    Gender             : int   = Field(..., ge=0, le=1)
    Ethnicity          : int   = Field(..., ge=0, le=3)
    EducationLevel     : int   = Field(..., ge=0, le=3)
    # Antécédents médicaux
    FamilyHistoryAlzheimers: int = Field(..., ge=0, le=1)
    CardiovascularDisease  : int = Field(..., ge=0, le=1)
    Diabetes               : int = Field(..., ge=0, le=1)
    Depression             : int = Field(..., ge=0, le=1)
    HeadInjury             : int = Field(..., ge=0, le=1)
    Hypertension           : int = Field(..., ge=0, le=1)
    # Biologie
    BMI                    : float = Field(..., ge=15, le=40)
    SystolicBP             : int   = Field(..., ge=90, le=180)
    DiastolicBP            : int   = Field(..., ge=60, le=120)
    CholesterolTotal       : float = Field(..., ge=150, le=300)
    CholesterolLDL         : float = Field(..., ge=50, le=200)
    CholesterolHDL         : float = Field(..., ge=20, le=100)
    CholesterolTriglycerides: float = Field(..., ge=50, le=400)
    # Habitudes de vie
    Smoking          : int   = Field(..., ge=0, le=1)
    AlcoholConsumption: float = Field(..., ge=0, le=20)
    PhysicalActivity : float = Field(..., ge=0, le=10)
    DietQuality      : float = Field(..., ge=0, le=10)
    SleepQuality     : float = Field(..., ge=0, le=10)
    # Autre
    Smoking          : int   = Field(..., ge=0, le=1)

class FactorItem(BaseModel):
    feature: str
    impact : float

class PredictionOutput(BaseModel):
    risk_score  : float
    prediction  : str
    severity    : str
    top_factors : List[FactorItem]
    alert       : bool