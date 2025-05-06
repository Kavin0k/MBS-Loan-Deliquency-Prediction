import streamlit as st
import joblib
import numpy as np

# Load model
model = joblib.load("xgb_model.pkl")

# Title
st.title("🏠 Mortgage Default Prediction")

# User Inputs
credit_score = st.number_input("Credit Score", min_value=0)
orig_upb = st.number_input("Original UPB", min_value=0.0)
dti = st.number_input("DTI", min_value=0.0)
ltv = st.number_input("LTV", min_value=0.0)
loan_age_months = st.number_input("Loan Age (Months)", min_value=0)
dti_per_unit = st.number_input("DTI per Unit", min_value=0.0)
monthly_principal = st.number_input("Monthly Principal", min_value=0.0)

# Predict button
if st.button("Predict Default"):
    features = np.array([[credit_score, orig_upb, dti, ltv, loan_age_months, dti_per_unit, monthly_principal]])
    prediction = model.predict(features)[0]
    if prediction == 1:
        st.error("⚠️ Likely to Default (Deliquent)")
    else:
        st.success("✅ Not Likely to Default")

