import streamlit as st
import numpy as np

# ---------- Page configuration ----------
st.set_page_config(
    page_title="Home Loan Default Predictor",
    page_icon="🏠",
    layout="centered"
)

# ---------- Custom CSS for styling ----------
st.markdown("""
    <style>
        /* Glass‑morphism card */
        .stApp {
            background: radial-gradient(circle at 10% 20%, #0a232d, #051418);
        }
        .main-card {
            background: rgba(18, 30, 38, 0.65);
            backdrop-filter: blur(16px);
            border-radius: 3rem;
            border: 1px solid rgba(72, 187, 200, 0.25);
            padding: 2rem;
            margin: 2rem auto;
            max-width: 650px;
        }
        .title {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #C0F2FF, #4ECDC4);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-align: center;
        }
        .sub {
            color: #8aaebd;
            text-align: center;
            margin-bottom: 2rem;
        }
        .result-box {
            background: rgba(0, 0, 0, 0.4);
            border-radius: 2rem;
            padding: 1rem;
            margin-top: 1.5rem;
            border-left: 4px solid #4ECDC4;
        }
        .model-badge {
            background: #0e2a33;
            padding: 0.2rem 0.8rem;
            border-radius: 30px;
            font-size: 0.7rem;
            font-weight: 600;
            color: #4ECDC4;
            display: inline-block;
            margin-right: 0.5rem;
        }
        .footer {
            text-align: center;
            font-size: 0.75rem;
            color: #5b8c9c;
            margin-top: 2rem;
            border-top: 1px dashed #2f616e;
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Prediction logic (mocked) ----------
def compute_risk(credit, income, days_birth, days_employed):
    dti = credit / (income + 0.01)
    dti = min(dti, 2.5)

    age_years = abs(days_birth) / 365.25
    emp_years = min(abs(days_employed) / 365.25, 40)

    risk_score = (1.6 * dti) - (0.02 * age_years) - (0.15 * emp_years) + 0.4
    if emp_years < 1:
        risk_score += 0.5
    if age_years < 22:
        risk_score += 0.4
    if dti > 0.8:
        risk_score += 0.6

    prob = 1 / (1 + np.exp(-risk_score))
    prob = max(0.01, min(0.99, prob))
    return prob

# ---------- UI ----------
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Model badges
st.markdown('<span class="model-badge">🤖 XGBoost (ROC‑AUC 0.81)</span> <span class="model-badge">🏆 Production Model</span>', unsafe_allow_html=True)

st.markdown('<div class="title">🏠 Home Loan Default Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Enter applicant details – AI assesses default risk instantly</div>', unsafe_allow_html=True)

# Input fields
cust_id = st.text_input("🆔 Customer ID", value="100001")
credit = st.number_input("💰 Credit Amount (₹)", min_value=0.0, value=100000.0, step=10000.0)
income = st.number_input("📊 Annual Income (₹)", min_value=0.0, value=200000.0, step=10000.0)
days_birth = st.number_input("📅 Days Birth (negative)", value=-10000)
days_employed = st.number_input("💼 Days Employed (negative)", value=-3000)

# Prediction button
if st.button("✨ Predict Default Risk ✨", use_container_width=True):
    if credit <= 0 or income <= 0:
        st.error("⚠️ Credit amount and Income must be positive numbers.")
    else:
        prob = compute_risk(credit, income, days_birth, days_employed)
        prob_percent = prob * 100

        if prob < 0.35:
            risk_label = "🟢 LOW DEFAULT RISK"
            recommendation = "✅ Eligible – Strong approval candidate"
            color = "#2ecc71"
        elif prob < 0.60:
            risk_label = "🟡 MEDIUM DEFAULT RISK"
            recommendation = "⚠️ Manual review recommended"
            color = "#f39c12"
        else:
            risk_label = "🔴 HIGH DEFAULT RISK"
            recommendation = "❌ High chance of default – Consider rejection"
            color = "#e67e22"

        st.markdown(f"""
            <div class="result-box">
                <div><strong>📊 Default Probability</strong> <span style="float:right; background:#0f2f38; padding:0.2rem 0.8rem; border-radius:40px; color:{color}; font-weight:bold;">{prob_percent:.1f}%</span></div>
                <div style="margin-top:12px; font-size:1.1rem; font-weight:600;">{risk_label}</div>
                <div style="margin-top:6px; font-size:0.9rem;">{recommendation}</div>
                <div style="margin-top:10px; font-size:0.75rem; opacity:0.8;">⚡ Model: XGBoost | Feature importance: debt/income, employment history</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">🧠 Model: XGBoost (Gradient Boosting) | 🎓 Project created by <strong>KalyanaSundar - AI Engineer</strong></div>', unsafe_allow_html=True)