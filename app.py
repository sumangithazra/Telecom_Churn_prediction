from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Annotated
from enum import Enum
import pandas as pd
import pickle

# =========================================================
# Load trained model and feature schema
# =========================================================
with open("churn_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model_features.pkl", "rb") as f:
    MODEL_FEATURES = pickle.load(f)

app = FastAPI(
    title="Telco Customer Churn Prediction API",
    description="Predicts customer churn using RandomForest + SMOTEENN",
    version="1.0"
)

# =========================================================
# Enums (Strict categorical control)
# =========================================================
class Gender(str, Enum):
    Male = "Male"
    Female = "Female"

class YesNo(str, Enum):
    Yes = "Yes"
    No = "No"

class InternetService(str, Enum):
    DSL = "DSL"
    Fiber = "Fiber optic"
    None_ = "No"

class Contract(str, Enum):
    Month = "Month-to-month"
    OneYear = "One year"
    TwoYear = "Two year"

class PaymentMethod(str, Enum):
    Electronic = "Electronic check"
    Mailed = "Mailed check"
    Bank = "Bank transfer (automatic)"
    Credit = "Credit card (automatic)"

# =========================================================
# Input Schema (RAW CSV-level features only)
# =========================================================
class CustomerInput(BaseModel):

    gender: Gender
    SeniorCitizen: Annotated[int, Field(ge=0, le=1)]
    Partner: YesNo
    Dependents: YesNo

    tenure: Annotated[int, Field(ge=0, le=72)]

    PhoneService: YesNo
    MultipleLines: str

    InternetService: InternetService
    OnlineSecurity: YesNo
    OnlineBackup: YesNo
    DeviceProtection: YesNo
    TechSupport: YesNo
    StreamingTV: YesNo
    StreamingMovies: YesNo

    Contract: Contract
    PaperlessBilling: YesNo
    PaymentMethod: PaymentMethod

    MonthlyCharges: Annotated[float, Field(gt=0)]
    TotalCharges: Annotated[float, Field(ge=0)]

    # ---------------- Business Rule Validation ----------------
    @field_validator("TotalCharges")
    @classmethod
    def total_charges_must_be_valid(cls, v, values):
        monthly = values.data.get("MonthlyCharges")
        if monthly is not None and v < monthly:
            raise ValueError("TotalCharges cannot be less than MonthlyCharges")
        return v

    # ---------------- Derived Feature ----------------
    @computed_field
    @property
    def tenure_group(self) -> str:
        if self.tenure < 12:
            return "1 - 11"
        elif self.tenure < 24:
            return "12 - 23"
        elif self.tenure < 36:
            return "24 - 35"
        elif self.tenure < 48:
            return "36 - 47"
        elif self.tenure < 60:
            return "48 - 59"
        else:
            return "60 - 71"

# =========================================================
# Prediction Endpoint
# =========================================================
@app.post("/predict")
def predict_churn(customer: CustomerInput):

    # Convert validated input → DataFrame
    df = pd.DataFrame([customer.model_dump()])

    # Drop tenure (only used for tenure_group)
    df.drop(columns=["tenure"], inplace=True)

    # One-hot encoding (same as training)
    df = pd.get_dummies(df)

    # Align with training feature space
    df = df.reindex(columns=MODEL_FEATURES, fill_value=0)

    # Model inference
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "churn_prediction": int(prediction),
        "churn_label": "Yes" if prediction == 1 else "No",
        "churn_probability": round(probability, 4)
    }
