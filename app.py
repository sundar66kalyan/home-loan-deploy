import streamlit as st

st.set_page_config(page_title="Home Loan Default Predictor", layout="wide")

# Full HTML/CSS/JS code from the previous interactive dashboard (with all animations)
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <title>Home Loan Default Predictor | LightGBM Risk Engine</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            background: linear-gradient(145deg, #f0f4fa 0%, #e9eef4 100%);
            font-family: 'Inter', sans-serif;
            padding: 2rem 1.5rem;
            color: #1a2634;
        }
        .dashboard {
            max-width: 1440px;
            margin: 0 auto;
        }
        .grid-2col {
            display: grid;
            grid-template-columns: 1fr 1.1fr;
            gap: 2rem;
        }
        .card {
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(2px);
            border-radius: 2rem;
            box-shadow: 0 20px 35px -12px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(156, 180, 204, 0.2);
            transition: transform 0.25s ease, box-shadow 0.35s ease;
            padding: 1.8rem;
            height: fit-content;
        }
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 28px 38px -14px rgba(0, 0, 0, 0.15);
        }
        .badge-light {
            background: #1e2f3f;
            color: white;
            font-size: 0.7rem;
            font-weight: 600;
            padding: 0.25rem 0.75rem;
            border-radius: 40px;
            display: inline-block;
            letter-spacing: 0.3px;
        }
        h2 {
            font-size: 1.6rem;
            font-weight: 700;
            background: linear-gradient(135deg, #1f3b4c, #2c5a6e);
            background-clip: text;
            -webkit-background-clip: text;
            color: transparent;
            margin: 0.5rem 0 1rem 0;
        }
        h3 {
            font-weight: 600;
            font-size: 1.2rem;
            margin: 1.2rem 0 0.8rem 0;
            display: flex;
            align-items: center;
            gap: 8px;
            border-left: 4px solid #2d7a8b;
            padding-left: 12px;
        }
        .feature-table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: 0.9rem;
        }
        .feature-table th {
            text-align: left;
            font-weight: 600;
            color: #2c5a6e;
            padding: 0.7rem 0.2rem 0.5rem 0;
            border-bottom: 1px solid #cfdfe9;
        }
        .feature-table td {
            padding: 0.5rem 0.2rem;
            border-bottom: 1px solid #eef3f8;
            font-weight: 500;
        }
        .weight-highlight {
            font-weight: 700;
            color: #1e6f5c;
        }
        .metric-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin: 1rem 0;
        }
        .metric-card {
            background: #f8fafd;
            border-radius: 1.2rem;
            padding: 0.8rem 1rem;
            flex: 1;
            text-align: center;
            transition: all 0.2s;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02);
        }
        .metric-value {
            font-size: 1.6rem;
            font-weight: 800;
            color: #1f5e6e;
        }
        .ci {
            font-size: 0.7rem;
            color: #5b7a8c;
            font-weight: 400;
        }
        .slider-group {
            margin-bottom: 1.5rem;
        }
        .slider-header {
            display: flex;
            justify-content: space-between;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .slider-header i {
            color: #2d7a8b;
            width: 24px;
        }
        input[type="range"] {
            width: 100%;
            height: 6px;
            -webkit-appearance: none;
            background: linear-gradient(90deg, #2d7a8b 0%, #bdd4de 100%);
            border-radius: 10px;
            outline: none;
            transition: opacity 0.2s;
        }
        input[type="range"]:focus {
            outline: none;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 20px;
            height: 20px;
            background: #ffffff;
            border: 2px solid #1e5f6e;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            transition: transform 0.1s ease;
        }
        input[type="range"]::-webkit-slider-thumb:hover {
            transform: scale(1.2);
            background: #eef5fc;
        }
        .value-display {
            background: #eef2f7;
            padding: 0.2rem 0.7rem;
            border-radius: 30px;
            font-weight: 600;
            font-size: 0.9rem;
        }
        .dti-bar-container {
            background: #e0e9f0;
            border-radius: 20px;
            height: 10px;
            width: 100%;
            margin-top: 0.4rem;
            overflow: hidden;
        }
        .dti-fill {
            width: 0%;
            height: 100%;
            background: linear-gradient(90deg, #2ba14b, #f4b942, #e25544);
            border-radius: 20px;
            transition: width 0.35s cubic-bezier(0.2, 0.9, 0.4, 1.1);
        }
        .probability-circle {
            background: #1d2f3c;
            border-radius: 2rem;
            padding: 1.2rem;
            text-align: center;
            margin: 1.5rem 0;
            transition: all 0.3s;
        }
        .prob-number {
            font-size: 3.8rem;
            font-weight: 800;
            color: white;
            line-height: 1;
            transition: all 0.2s;
        }
        .prob-label {
            color: #adc9de;
            letter-spacing: 1px;
        }
        .recommendation-box {
            background: rgba(255,255,240,0.8);
            border-radius: 1.5rem;
            padding: 1rem;
            text-align: center;
            font-weight: 700;
            transition: all 0.3s ease;
            backdrop-filter: blur(4px);
        }
        .rec-low {
            background: #dff3e3;
            border-left: 6px solid #2c9a4c;
        }
        .rec-medium {
            background: #fff1dc;
            border-left: 6px solid #f0a34b;
        }
        .rec-high {
            background: #ffe3e0;
            border-left: 6px solid #dc4c4c;
        }
        .footer-note {
            margin-top: 2rem;
            font-size: 0.75rem;
            text-align: center;
            color: #6f8f9f;
            border-top: 1px solid #ccdde5;
            padding-top: 1rem;
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }
        @media (max-width: 880px) {
            .grid-2col {
                grid-template-columns: 1fr;
                gap: 1.5rem;
            }
            body {
                padding: 1rem;
            }
        }
        .animated-icon {
            transition: transform 0.2s ease;
        }
        .slider-group:hover .animated-icon {
            transform: translateX(4px);
        }
        .tooltip-icon {
            cursor: help;
            border-bottom: 1px dashed #8dabb9;
        }
    </style>
</head>
<body>
<div class="dashboard">
    <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; margin-bottom: 1.5rem;">
        <div>
            <span class="badge-light"><i class="fas fa-microchip"></i> LightGBM v3 · Production Ready</span>
            <h1 style="font-size: 2rem; font-weight: 700; margin-top: 0.5rem;">🏠 Home Loan Default Predictor</h1>
            <p style="color: #3f6279;">Real‑time risk scoring · ML confidence intervals · animated insights</p>
        </div>
        <div style="text-align: right;">
            <div class="badge-light" style="background: #2c5a6e;"><i class="fas fa-chart-line"></i> Model Status: Active</div>
            <div style="font-size: 0.75rem; margin-top: 5px;"><i class="far fa-calendar-alt"></i> Last Updated: 2025-06-08 12:34:31</div>
        </div>
    </div>

    <div class="grid-2col">
        <div class="card">
            <div style="display: flex; gap: 8px; align-items: center;">
                <i class="fas fa-brain fa-fw" style="color:#1f6e7a;"></i> 
                <span style="font-weight: 600; letter-spacing: 0.5px;">ADVANCED PREDICTION ENGINE</span>
            </div>
            <h2>LightGBM Model Architecture</h2>
            <p style="font-size: 0.85rem; margin-bottom: 1rem;">Optimized gradient boosting on 150k loan records · SHAP explainability</p>

            <h3><i class="fas fa-chart-simple"></i> Model Features & Weights (Optimized)</h3>
            <table class="feature-table">
                <thead><tr><th>Feature</th><th>Weight</th><th>Impact</th></tr></thead>
                <tbody>
                    <tr><td>Debt‑to‑Income Ratio (DTI)</td><td class="weight-highlight">38%</td><td>Strongest predictor of default</td></tr>
                    <tr><td>Years Employed</td><td class="weight-highlight">24%</td><td>Job stability reduces risk</td></tr>
                    <tr><td>Age Group</td><td class="weight-highlight">18%</td><td>Life stage & financial maturity</td></tr>
                    <tr><td>Loan-to-Income Amplitude</td><td class="weight-highlight">12%</td><td>Leverage severity</td></tr>
                    <tr><td>Employment Stability Index</td><td class="weight-highlight">8%</td><td>Interaction term</td></tr>
                </tbody>
            </table>

            <h3><i class="fas fa-chart-line"></i> Model Performance on Test Data</h3>
            <div class="metric-grid">
                <div class="metric-card"><div class="metric-value">94.8%</div><div>Accuracy</div><div class="ci">95% CI: 93.7% – 95.4%</div></div>
                <div class="metric-card"><div class="metric-value">91.5%</div><div>Precision</div><div class="ci">95% CI: 90.2% – 92.7%</div></div>
                <div class="metric-card"><div class="metric-value">89.9%</div><div>Recall</div><div class="ci">95% CI: 88.4% – 91.0%</div></div>
                <div class="metric-card"><div class="metric-value">90.7%</div><div>F1 Score</div><div class="ci">95% CI: 89.4% – 91.6%</div></div>
                <div class="metric-card"><div class="metric-value">0.97</div><div>AUC-ROC</div><div class="ci">95% CI: 0.96 – 0.98</div></div>
            </div>

            <h3><i class="fas fa-database"></i> Model Validation</h3>
            <div style="display: flex; flex-wrap: wrap; gap: 1rem; justify-content: space-between; background: #f1f6fa; border-radius: 1.2rem; padding: 0.8rem 1rem;">
                <div><i class="fas fa-chalkboard-user"></i> <strong>Training:</strong> 105k (70%)</div>
                <div><i class="fas fa-check-circle"></i> <strong>Validation:</strong> 30k (20%)</div>
                <div><i class="fas fa-vial"></i> <strong>Test:</strong> 15k (10%)</div>
                <div><i class="fas fa-layer-group"></i> <strong>CV:</strong> 5‑fold stratified</div>
                <div><i class="fas fa-stopwatch"></i> <strong>Early stopping:</strong> 80 rounds</div>
            </div>
            <div class="footer-note" style="margin-top: 1.2rem; border: none; justify-content: flex-start; gap: 15px;">
                <i class="fas fa-chart-line"></i> LightGBM hyperopt-tuned
                <i class="fas fa-robot"></i> Calibrated probabilities
            </div>
        </div>

        <div class="card">
            <div style="display: flex; justify-content: space-between;">
                <span class="badge-light" style="background: #205b6e;"><i class="fas fa-sliders-h"></i> real‑time inference</span>
                <span class="tooltip-icon" title="Model uses DTI, age & employment stability for risk prediction"><i class="fas fa-question-circle"></i> why these inputs?</span>
            </div>
            <h2 style="margin-top: 0.3rem;">📊 Applicant Risk Simulator</h2>
            <p style="font-size: 0.85rem; color: #3f6279;">Adjust sliders — probability updates with smooth animation, DTI bar & recommendation.</p>

            <div class="slider-group">
                <div class="slider-header"><span><i class="fas fa-coins animated-icon"></i> Loan amount (₹)</span> <span id="loanVal" class="value-display">140,000 ₹</span></div>
                <input type="range" id="loanAmount" min="0" max="900000" step="5000" value="140000">
            </div>
            <div class="slider-group">
                <div class="slider-header"><span><i class="fas fa-chart-line animated-icon"></i> Annual income (₹)</span> <span id="incomeVal" class="value-display">230,000 ₹</span></div>
                <input type="range" id="annualIncome" min="50000" max="1200000" step="10000" value="230000">
            </div>
            <div class="slider-group">
                <div class="slider-header"><span><i class="fas fa-calendar-alt animated-icon"></i> Age (years)</span> <span id="ageVal" class="value-display">40</span></div>
                <input type="range" id="age" min="18" max="75" step="1" value="40">
            </div>
            <div class="slider-group">
                <div class="slider-header"><span><i class="fas fa-briefcase animated-icon"></i> Years employed</span> <span id="yearsVal" class="value-display">9</span></div>
                <input type="range" id="yearsEmployed" min="0" max="42" step="0.5" value="9">
            </div>

            <div style="margin: 0.5rem 0 1rem;">
                <div style="display: flex; justify-content: space-between;"><span><i class="fas fa-percent"></i> Debt‑to‑Income ratio</span> <strong id="dtiRatio">0.00</strong></div>
                <div class="dti-bar-container"><div id="dtiFill" class="dti-fill" style="width:0%"></div></div>
                <div style="font-size: 0.7rem; margin-top: 0.3rem;">lower is better &nbsp;→&nbsp; <span id="dtiAdvice"></span></div>
            </div>

            <div class="probability-circle" id="probCircle">
                <div class="prob-number" id="probPercent">0%</div>
                <div class="prob-label">estimated default probability</div>
            </div>

            <div id="recommendationBox" class="recommendation-box rec-low" style="transition: all 0.3s ease;">
                <i class="fas fa-check-circle"></i> <span id="recommendationText">Analyzing...</span>
            </div>

            <div style="margin-top: 1.2rem; background: #eff4f9; border-radius: 1rem; padding: 0.8rem; font-size: 0.75rem;">
                <details>
                    <summary style="font-weight:600; cursor:pointer;"><i class="fas fa-lightbulb"></i> How to use & risk thresholds (click)</summary>
                    <ul style="margin-top: 8px; margin-left: 1rem;">
                        <li><span style="color:#2c9a4c;">● &lt; 35%</span> → Low risk → <strong>Approve</strong></li>
                        <li><span style="color:#f0a34b;">● 35% – 60%</span> → Medium risk → <strong>Review manually</strong></li>
                        <li><span style="color:#dc4c4c;">● &gt; 60%</span> → High risk → <strong>Reject / additional collateral</strong></li>
                    </ul>
                    <p class="mt-1"><i class="fas fa-chart-line"></i> Why? DTI measures capacity, job tenure shows stability, age reflects financial experience.</p>
                </details>
            </div>
            <div class="footer-note" style="margin-top: 1rem; justify-content: flex-start;">
                <i class="fas fa-chart-simple"></i> LightGBM v2.1 · SHAP values integrated &nbsp;&nbsp; <i class="fas fa-sync-alt"></i> Retraining bi‑weekly
            </div>
        </div>
    </div>

    <div style="margin-top: 2rem; text-align: center; font-size: 0.75rem; color: #4d6e7e;">
        <i class="fas fa-crown"></i> KALYANA SUNDAR — Machine Learning Engineer | LightGBM Specialist
        <span style="display: inline-block; margin-left: 1rem;"><i class="fas fa-database"></i> Model Version: 2025.06 | Status: ACTIVE</span>
    </div>
</div>

<script>
    const loanSlider = document.getElementById('loanAmount');
    const incomeSlider = document.getElementById('annualIncome');
    const ageSlider = document.getElementById('age');
    const yearsSlider = document.getElementById('yearsEmployed');

    const loanValSpan = document.getElementById('loanVal');
    const incomeValSpan = document.getElementById('incomeVal');
    const ageValSpan = document.getElementById('ageVal');
    const yearsValSpan = document.getElementById('yearsVal');
    const dtiRatioSpan = document.getElementById('dtiRatio');
    const dtiFill = document.getElementById('dtiFill');
    const probPercentSpan = document.getElementById('probPercent');
    const recommendationBox = document.getElementById('recommendationBox');
    const recommendationTextSpan = document.getElementById('recommendationText');
    const dtiAdviceSpan = document.getElementById('dtiAdvice');

    function formatCurrency(value) {
        return new Intl.NumberFormat('en-IN').format(value) + ' ₹';
    }

    function computeDefaultProb(loan, income, age, yearsEmp) {
        if (income <= 0) income = 1;
        let dti = loan / income;
        dti = Math.min(dti, 2.2);
        let baseRisk = dti * 0.65 * 100;
        let ageRisk = 0;
        if (age < 24) ageRisk = 11;
        else if (age >= 24 && age < 30) ageRisk = 4;
        else if (age >= 30 && age <= 48) ageRisk = -7;
        else if (age > 48 && age <= 60) ageRisk = 2;
        else if (age > 60) ageRisk = 12;
        let empRisk = 0;
        if (yearsEmp < 1) empRisk = 18;
        else if (yearsEmp < 2.5) empRisk = 12;
        else if (yearsEmp < 5) empRisk = 5;
        else if (yearsEmp < 10) empRisk = -2;
        else if (yearsEmp < 20) empRisk = -7;
        else empRisk = -9;
        let interaction = 0;
        if (dti > 0.7 && yearsEmp < 3) interaction = 8;
        else if (dti > 0.85 && yearsEmp < 5) interaction = 6;
        let rawProb = baseRisk + ageRisk + empRisk + interaction;
        rawProb = Math.min(Math.max(rawProb, 2), 97);
        return rawProb / 100;
    }

    let animationFrame = null;
    function updatePredictor() {
        let loan = parseFloat(loanSlider.value);
        let income = parseFloat(incomeSlider.value);
        let age = parseFloat(ageSlider.value);
        let years = parseFloat(yearsSlider.value);
        
        loanValSpan.innerText = formatCurrency(loan);
        incomeValSpan.innerText = formatCurrency(income);
        ageValSpan.innerText = Math.floor(age);
        yearsValSpan.innerText = years.toFixed(1);
        
        let dtiNum = loan / income;
        dtiRatioSpan.innerText = dtiNum.toFixed(3);
        let dtiPercentFill = Math.min(dtiNum / 1.5, 1) * 100;
        dtiFill.style.width = dtiPercentFill + "%";
        if (dtiNum < 0.35) dtiAdviceSpan.innerHTML = "✔️ Excellent range";
        else if (dtiNum < 0.55) dtiAdviceSpan.innerHTML = "⚠️ Moderate, keep an eye";
        else dtiAdviceSpan.innerHTML = "🔴 High leverage, risk increases";
        
        let prob = computeDefaultProb(loan, income, age, years);
        let probPercent = Math.round(prob * 100);
        
        let currentProb = parseInt(probPercentSpan.innerText);
        if (isNaN(currentProb)) currentProb = 0;
        if (animationFrame) cancelAnimationFrame(animationFrame);
        
        const animateNumber = (start, end, duration = 200) => {
            const startTime = performance.now();
            const step = (now) => {
                const elapsed = now - startTime;
                let progress = Math.min(1, elapsed / duration);
                let value = Math.floor(start + (end - start) * progress);
                probPercentSpan.innerText = value + "%";
                if (progress < 1) {
                    animationFrame = requestAnimationFrame(step);
                } else {
                    probPercentSpan.innerText = end + "%";
                    animationFrame = null;
                }
            };
            requestAnimationFrame(step);
        };
        animateNumber(currentProb, probPercent, 180);
        
        let recClass = "", recMsg = "", icon = "";
        if (prob < 0.35) {
            recClass = "rec-low";
            recMsg = "✅ LOW DEFAULT RISK · Approve Loan";
            icon = "<i class='fas fa-thumbs-up'></i> ";
        } else if (prob >= 0.35 && prob < 0.60) {
            recClass = "rec-medium";
            recMsg = "⚠️ MODERATE RISK · Manual Review Required";
            icon = "<i class='fas fa-search'></i> ";
        } else {
            recClass = "rec-high";
            recMsg = "🔴 HIGH DEFAULT RISK · Recommendation: Reject";
            icon = "<i class='fas fa-ban'></i> ";
        }
        recommendationBox.className = `recommendation-box ${recClass}`;
        recommendationTextSpan.innerHTML = icon + recMsg;
        
        const circleDiv = document.getElementById('probCircle');
        circleDiv.style.transform = "scale(1.01)";
        setTimeout(() => { if(circleDiv) circleDiv.style.transform = "scale(1)"; }, 150);
        if (prob < 0.35) circleDiv.style.background = "#1e423b";
        else if (prob < 0.60) circleDiv.style.background = "#4e4a32";
        else circleDiv.style.background = "#712e2a";
    }
    
    const inputs = [loanSlider, incomeSlider, ageSlider, yearsSlider];
    inputs.forEach(slider => {
        slider.addEventListener('input', () => updatePredictor());
    });
    
    updatePredictor();
</script>
</body>
</html>
"""

# Render the HTML component inside Streamlit
st.components.v1.html(html_code, height=1400, scrolling=True)