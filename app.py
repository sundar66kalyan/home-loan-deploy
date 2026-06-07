import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model
model = joblib.load("models/best_xgboost_credit_model.pkl")

st.set_page_config(page_title="Home Loan Default Predictor", layout="wide")

st.title("🏦 Home Loan Default Prediction App")

st.write("Enter applicant details to predict loan default risk")

# Example inputs (replace with your real features)
SK_ID_CURR = st.number_input("Customer ID", value=100001)
AMT_CREDIT = st.number_input("Credit Amount", value=100000.0)
AMT_INCOME_TOTAL = st.number_input("Income", value=200000.0)
DAYS_BIRTH = st.number_input("Days Birth", value=-10000)
DAYS_EMPLOYED = st.number_input("Days Employed", value=-3000)

# Create input dataframe
input_data = pd.DataFrame([[
    SK_ID_CURR,
    AMT_CREDIT,
    AMT_INCOME_TOTAL,
    DAYS_BIRTH,
    DAYS_EMPLOYED
]], columns=[
    "SK_ID_CURR",
    "AMT_CREDIT",
    "AMT_INCOME_TOTAL",
    "DAYS_BIRTH",
    "DAYS_EMPLOYED"
])

if st.button("Predict"):
    prediction = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][1]

    st.success(f"Prediction: {'Default Risk' if prediction==1 else 'No Default Risk'}")
    st.info(f"Default Probability: {prob:.4f}")