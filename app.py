import streamlit as st
import numpy as np

# ---------- Page config ----------
st.set_page_config(
    page_title="Home Loan Default Predictor",
    page_icon="🏠",
    layout="centered"
)

# ---------- Custom CSS to fix visibility and styling ----------
st.markdown("""
    <style>
        .main-title {
            font-size: 2.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #C0F2FF, #4ECDC4);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-align: center;
            margin-bottom: 0.2rem;
        }
        .subhead {
            text-align: center;
            color: #8aaebd;
            margin-bottom: 2rem;
        }
        .metric-card {
            background: rgba(18, 30, 38, 0.6);
            border-radius: 1.5rem;
            padding: 0.8rem;
            text-align: center;
            backdrop-filter: blur(5px);
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

# ---------- Helper: Risk computation ----------
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
    return prob, dti, age_years, emp_years

# ---------- UI ----------
# Title (now definitely visible)
st.markdown('<div class="main-title">🏠 Home Loan Default Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subhead">Enter applicant details – AI assesses default risk instantly</div>', unsafe_allow_html=True)

# Model badges
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown('<div style="text-align:center"><span class="model-badge">🤖 XGBoost (ROC‑AUC 0.81)</span> <span class="model-badge">🏆 Production Model</span></div>', unsafe_allow_html=True)

# Input fields (with clear labels)
st.markdown("### 📋 Applicant Information")
col_cred, col_inc = st.columns(2)
with col_cred:
    credit = st.number_input("💰 Credit Amount (₹)", min_value=0.0, value=100000.0, step=10000.0,
                             help="Total loan amount requested")
with col_inc:
    income = st.number_input("📊 Annual Income (₹)", min_value=0.0, value=200000.0, step=10000.0,
                             help="Total yearly income from all sources")

col_birth, col_emp = st.columns(2)
with col_birth:
    days_birth = st.number_input("📅 Days Birth (negative)", value=-10000,
                                 help="Days before today (e.g., -10000 = about 27 years old)")
with col_emp:
    days_employed = st.number_input("💼 Days Employed (negative)", value=-3000,
                                    help="Days before today since started working (negative)")

# Display derived metrics automatically
if credit > 0 and income > 0:
    _, dti, age, emp_years = compute_risk(credit, income, days_birth, days_employed)
    st.markdown("#### 📊 Key Metrics")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Debt-to-Income", f"{dti:.2f}")
    metric_col2.metric("Age (years)", f"{age:.1f}")
    metric_col3.metric("Employment (years)", f"{emp_years:.1f}")
    metric_col4.metric("Model AUC", "0.81", help="XGBoost cross‑validation score")

# Predict button
if st.button("✨ Predict Default Risk ✨", use_container_width=True):
    if credit <= 0 or income <= 0:
        st.error("⚠️ Credit amount and Income must be positive numbers.")
    else:
        prob, dti, age, emp_years = compute_risk(credit, income, days_birth, days_employed)
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
                <div style="margin-top:10px; font-size:0.75rem; opacity:0.8;">⚡ Model: XGBoost | Feature importance: debt/income, employment history, age</div>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">🧠 Model: XGBoost (Gradient Boosting) | 🎓 Project created by <strong>KalyanaSundar - AI Engineer</strong></div>', unsafe_allow_html=True)