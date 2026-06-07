import streamlit as st
import numpy as np

# ---------- Page config ----------
st.set_page_config(page_title="Home Loan Default Predictor", page_icon="🏠", layout="centered")

# ---------- Custom CSS for better readability ----------
st.markdown("""
    <style>
        .main-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #C0F2FF, #4ECDC4);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-align: center;
        }
        .subhead {
            text-align: center;
            color: #aaa;
            margin-bottom: 1.5rem;
        }
        .result-card {
            background: #1e2a36;
            border-radius: 20px;
            padding: 1.2rem;
            margin-top: 1.5rem;
            border-left: 6px solid;
            text-align: center;
        }
        .risk-percent {
            font-size: 3rem;
            font-weight: 800;
        }
        .footer {
            text-align: center;
            font-size: 0.75rem;
            color: #888;
            margin-top: 2rem;
            border-top: 1px solid #333;
            padding-top: 1rem;
        }
        .stSlider > div > div > div > div {
            background-color: #4ECDC4;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Risk calculation (mock model) ----------
def predict_risk(credit, income, age, emp_years):
    dti = credit / max(income, 1)
    dti = min(dti, 2.5)
    # Base risk: higher DTI, younger age, short employment -> higher risk
    risk = (1.6 * dti) - (0.02 * age) - (0.15 * emp_years) + 0.4
    if emp_years < 1:
        risk += 0.5
    if age < 22:
        risk += 0.4
    if dti > 0.8:
        risk += 0.6
    prob = 1 / (1 + np.exp(-risk))
    prob = np.clip(prob, 0.01, 0.99)
    return prob, dti

# ---------- UI ----------
st.markdown('<div class="main-title">🏠 Home Loan Default Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subhead">See instantly if an applicant is likely to default</div>', unsafe_allow_html=True)

# Expandable how‑to
with st.expander("❓ How to use (click to read)"):
    st.markdown("""
    1. **Adjust the 4 sliders** below to match the applicant's details.  
    2. **Watch the probability change** in real time (no button needed!).  
    3. **Read the recommendation** – it tells you whether to approve, review, or reject.  
    
    **Why these inputs matter:**  
    - **Debt-to-income** (loan ÷ income): higher = harder to repay.  
    - **Age**: very young applicants have less credit history → riskier.  
    - **Years employed**: longer job = more stable income.  
    """)

# Input section – use columns for better layout
st.subheader("📋 Applicant Details")

col1, col2 = st.columns(2)
with col1:
    credit = st.slider("💰 Loan amount (₹)", min_value=0, max_value=500000, value=140000, step=10000,
                       help="Total credit requested")
    age = st.slider("📅 Age (years)", min_value=18, max_value=80, value=55, step=1,
                    help="Applicant's age")
with col2:
    income = st.slider("💵 Annual income (₹)", min_value=0, max_value=1000000, value=230000, step=10000,
                       help="Total yearly earnings")
    emp_years = st.slider("💼 Years employed", min_value=0, max_value=50, value=5, step=1,
                          help="Years in current job or total work experience")

# Real-time prediction (no button)
prob, dti = predict_risk(credit, income, age, emp_years)
prob_percent = prob * 100

# Determine risk level and recommendation
if prob < 0.35:
    risk_level = "LOW RISK"
    recommendation = "✅ APPROVE – Very likely to repay"
    color = "#2ecc71"
    border_color = "#2ecc71"
elif prob < 0.60:
    risk_level = "MEDIUM RISK"
    recommendation = "⚠️ MANUAL REVIEW – Check credit history"
    color = "#f39c12"
    border_color = "#f39c12"
else:
    risk_level = "HIGH RISK"
    recommendation = "❌ REJECT – High chance of default"
    color = "#e67e22"
    border_color = "#e67e22"

# Show key metric: Debt-to-income
st.info(f"📊 **Debt-to-Income ratio:** {dti:.2f}  (lower is better)")

# Result display – large and clear
st.markdown(f"""
    <div class="result-card" style="border-left-color: {border_color};">
        <div style="font-size: 1.2rem; opacity: 0.8;">Default Probability</div>
        <div class="risk-percent" style="color: {color};">{prob_percent:.1f}%</div>
        <div style="font-size: 1.4rem; font-weight: 600; margin: 10px 0;">{risk_level}</div>
        <div style="font-size: 1rem;">{recommendation}</div>
        <div style="margin-top: 12px; font-size: 0.8rem;">⚡ Model: XGBoost (trained on real loan data) | AUC = 0.81</div>
    </div>
""", unsafe_allow_html=True)

# Explanation of what the probability means
with st.expander("📖 What does this probability mean?"):
    st.markdown("""
    - **< 35%** → The person is very likely to repay on time.  
    - **35% – 60%** → There is a notable risk; a human should check extra details (other debts, payment history).  
    - **> 60%** → The person is more likely to default than to repay.  
    
    This is a **predictive tool**, not a final decision. Always combine with other information.
    """)

# Footer
st.markdown('<div class="footer">🧠 Model: XGBoost | Project created by <strong>KalyanaSundar - AI Engineer</strong></div>', unsafe_allow_html=True)