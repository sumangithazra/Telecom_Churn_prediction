import streamlit as st
import requests

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Telco Churn Predictor",
    layout="centered"
)

st.title("📞 Telco Customer Churn Prediction")
st.markdown("Enter customer details to predict churn probability.")

API_URL = "http://127.0.0.1:8000/predict"

# -------------------------------------------------
# Input Form
# -------------------------------------------------
with st.form("churn_form"):

    gender = st.selectbox("Gender", ["Male", "Female"])
    SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
    Partner = st.selectbox("Partner", ["Yes", "No"])
    Dependents = st.selectbox("Dependents", ["Yes", "No"])

    tenure = st.slider("Tenure (months)", 0, 72, 12)

    PhoneService = st.selectbox("Phone Service", ["Yes", "No"])
    MultipleLines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])

    InternetService = st.selectbox(
        "Internet Service", ["DSL", "Fiber optic", "No"]
    )

    OnlineSecurity = st.selectbox("Online Security", ["Yes", "No"])
    OnlineBackup = st.selectbox("Online Backup", ["Yes", "No"])
    DeviceProtection = st.selectbox("Device Protection", ["Yes", "No"])
    TechSupport = st.selectbox("Tech Support", ["Yes", "No"])
    StreamingTV = st.selectbox("Streaming TV", ["Yes", "No"])
    StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No"])

    Contract = st.selectbox(
        "Contract", ["Month-to-month", "One year", "Two year"]
    )

    PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])

    PaymentMethod = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    MonthlyCharges = st.number_input(
        "Monthly Charges", min_value=0.0, step=1.0
    )
    TotalCharges = st.number_input(
        "Total Charges", min_value=0.0, step=10.0
    )

    submitted = st.form_submit_button("Predict Churn")

# -------------------------------------------------
# API Call
# -------------------------------------------------
if submitted:

    payload = {
        "gender": gender,
        "SeniorCitizen": SeniorCitizen,
        "Partner": Partner,
        "Dependents": Dependents,
        "tenure": tenure,
        "PhoneService": PhoneService,
        "MultipleLines": MultipleLines,
        "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport,
        "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies,
        "Contract": Contract,
        "PaperlessBilling": PaperlessBilling,
        "PaymentMethod": PaymentMethod,
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)

        if response.status_code == 200:
            result = response.json()

            churn_label = result["churn_label"]
            churn_prob = result["churn_probability"]

            if churn_label == "Yes":
                st.error(
                    f"⚠️ Customer is likely to churn\n\n"
                    f"**Probability:** {churn_prob:.2%}"
                )
            else:
                st.success(
                    f"✅ Customer is likely to stay\n\n"
                    f"**Probability:** {churn_prob:.2%}"
                )

        elif response.status_code == 422:
            st.warning("⚠️ Validation error. Please check input values.")
            st.json(response.json())

        else:
            st.error("❌ API error occurred")
            st.text(response.text)

    except requests.exceptions.ConnectionError:
        st.error("❌ Backend API is not running. Start FastAPI first.")
