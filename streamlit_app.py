import streamlit as st
import requests

# Flask API endpoint
API_URL = "http://127.0.0.1:5000/predict"  # Change this URL if deployed elsewhere

st.title("Loan Delinquency Prediction App 📉")

st.markdown("### Enter Applicant Details")

# User Inputs for all required features
credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=650)
orig_upb = st.number_input("Original UPB (Loan Balance)", min_value=0.0, value=200000.0)
dti = st.number_input("Debt-to-Income Ratio (%)", min_value=0.0, value=36.0)
ltv = st.number_input("Loan-to-Value Ratio (%)", min_value=0.0, value=80.0)
loan_age_months = st.number_input("Loan Age (Months)", min_value=0, value=24)
dti_per_unit = st.number_input("DTI per Unit", min_value=0.0, value=0.5)
monthly_principal = st.number_input("Monthly Principal Payment", min_value=0.0, value=1000.0)

# Predict Button
if st.button("Predict Delinquency"):
    # Prepare input as JSON
    input_data = {
        "CreditScore": credit_score,
        "OrigUPB": orig_upb,
        "DTI": dti,
        "LTV": ltv,
        "LoanAgeMonths": loan_age_months,
        "DTI_per_Unit": dti_per_unit,
        "MonthlyPrincipal": monthly_principal
    }

    try:
        # Send data to Flask API
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if "prediction" in result:
            prediction = result["prediction"][0]
            if prediction == 1:
                st.error("⚠️ High Risk: The loan is likely to be *delinquent*.")
            else:
                st.success("✅ Low Risk: The loan is *not likely* to be delinquent.")
        else:
            st.error(f"API Error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Request failed: {e}")
