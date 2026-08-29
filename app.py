import streamlit as st
import requests
import plotly.graph_objects as go
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="SANKET - Personnel Wellness System",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS for Modern Defense Command Center Header & Layout
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .header-banner {
        background: linear-gradient(135deg, #161b22 0%, #1f242c 100%);
        padding: 22px 26px;
        border-radius: 14px;
        border: 1px solid #30363d;
        border-left: 5px solid #58a6ff;
        margin-bottom: 25px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.6);
    }
    .stForm {
        background-color: #161b22;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    h1, h2, h3 {
        color: #f0f6fc;
    }
    .metric-container {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Sleek Command Center Header Banner (Fixed Badge Wrapping)
st.markdown("""
    <div class="header-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div>
                <h1 style="margin: 0; font-size: 26px; color: #f0f6fc; display: flex; align-items: center; gap: 10px;">
                    🛡️ SANKET : Operational Fatigue Intelligence
                </h1>
                <p style="margin: 6px 0 0 0; color: #8b949e; font-size: 12px; font-weight: 500; letter-spacing: 0.5px;">
                    MINISTRY OF HOME AFFAIRS &nbsp;|&nbsp; OPERATIONAL WELLNESS & FATIGUE RISK ENGINE
                </p>
            </div>
            <div>
                <span style="background-color: #238636; color: white; padding: 6px 14px; border-radius: 20px; font-size: 11px; font-weight: bold; letter-spacing: 1px; border: 1px solid #2ea043; white-space: nowrap; display: inline-block;">
                    ● SECURE NODE ACTIVE
                </span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

with st.form("jawan_form"):
    st.subheader("📋 Enter Operational Parameters")
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        duty_hours = st.slider("Duty Hours Today", 0.0, 24.0, 10.0, step=0.5)
        sleep_duration = st.slider("Sleep Duration (Hours)", 0.0, 24.0, 6.0, step=0.5)
        temperature_c = st.number_input("Environment Temperature (°C)", min_value=-50.0, max_value=60.0, value=25.0, step=1.0)
        service_years = st.number_input("Service Years", min_value=0, max_value=45, value=5, step=1)
        
    with col2:
        force_type = st.selectbox("Force Type", ["BSF", "CRPF", "ITBP", "CISF", "SSB", "Assam_Rifles"])
        role = st.selectbox("Operational Role", ["GD_Patrol", "QRT_SpecialOps", "Support_Tech"])
        region = st.selectbox("Deployment Region", ["High_Altitude", "Naxal_Forest", "Desert", "Urban_Plains", "Industrial_Belt", "Forest_Foothills"])
        connectivity_status = st.selectbox("Connectivity Status", ["Full", "Blackout"])

    st.markdown("---")
    avg_duty_7d = st.slider("📉 7-Day Average Duty Hours (Chronic Load)", 0.0, 24.0, 6.0, step=0.5)
    
    st.markdown("")
    submit_button = st.form_submit_button(label="🚀 Evaluate Fatigue Risk", use_container_width=True)

if submit_button:
    payload = {
        "duty_hours": duty_hours,
        "sleep_duration": sleep_duration,
        "temperature_c": temperature_c,
        "service_years": service_years,
        "force_type": force_type,
        "role": role,
        "region": region,
        "connectivity_status": connectivity_status,
        "avg_duty_7d": avg_duty_7d
    }
    
    with st.spinner("Analyzing operational telemetry across secure nodes..."):
        try:
            response = requests.post("http://127.0.0.1:8000/predict", json=payload)
            if response.status_code == 200:
                res_data = response.json()
                risk = res_data["predicted_risk_category"]
                confidence_pct = round(res_data["confidence_score"] * 100, 1)
                
                # --- Fine-Tuned Continuous Threat Index Calculation ---
                raw_calc = (
                    (duty_hours / 2.8) + 
                    (np.clip(8.0 - sleep_duration, 0, 6) * 0.9) + 
                    (avg_duty_7d / 3.2)
                )
                if connectivity_status == "Blackout":
                    raw_calc += 1.2
                if region in ["High_Altitude", "Naxal_Forest"]:
                    raw_calc += 0.8
                
                if risk == "LOW":
                    risk_val = round(float(min(max(raw_calc, 1.0), 4.4)), 1)
                    gauge_color = "#28a745"
                elif risk == "MEDIUM":
                    risk_val = round(float(min(max(raw_calc, 4.5), 7.4)), 1)
                    gauge_color = "#ffc107"
                else:
                    risk_val = round(float(min(max(raw_calc, 7.5), 10.0)), 1)
                    gauge_color = "#dc3545"
                # ----------------------------------------------------
                
                st.markdown("---")
                st.subheader("📊 Tactical HUD & Telemetry Analysis")
                
                # Plotly Speedometer / Gauge Chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = risk_val,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': f"<b>Threat Index Level ({risk})</b>", 'font': {'color': '#f0f6fc', 'size': 18}},
                    number = {'font': {'color': '#f0f6fc', 'size': 40}, 'suffix': " / 10"},
                    gauge = {
                        'axis': {'range': [0, 10], 'tickwidth': 2, 'tickcolor': "#8b949e"},
                        'bar': {'color': gauge_color, 'thickness': 0.3},
                        'bgcolor': "#161b22",
                        'borderwidth': 2,
                        'bordercolor': "#30363d",
                        'steps': [
                            {'range': [0, 4.5], 'color': 'rgba(40, 167, 69, 0.15)'},
                            {'range': [4.5, 7.5], 'color': 'rgba(255, 193, 7, 0.15)'},
                            {'range': [7.5, 10], 'color': 'rgba(220, 53, 69, 0.15)'}
                        ],
                        'threshold': {
                            'line': {'color': "#ff4444", 'width': 4},
                            'thickness': 0.8,
                            'value': 7.5
                        }
                    }
                ))
                
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={'color': "white", 'family': "sans-serif"},
                    height=280,
                    margin=dict(t=40, b=10, l=20, r=20)
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                
                # Styled Metrics Cards Layout
                c1, c2 = st.columns(2, gap="medium")
                with c1:
                    st.markdown(f"""
                        <div class="metric-container">
                            <p style="color: #8b949e; margin-bottom: 2px; font-size: 14px;">MODEL CONFIDENCE</p>
                            <h2 style="color: #58a6ff; margin-top: 0;">{confidence_pct}%</h2>
                        </div>
                    """, unsafe_allow_html=True)
                with c2:
                    load_label = "CRITICAL OVERLOAD" if avg_duty_7d > 12 else "NORMAL ROUTINE"
                    load_color = "#f85149" if avg_duty_7d > 12 else "#3fb950"
                    st.markdown(f"""
                        <div class="metric-container">
                            <p style="color: #8b949e; margin-bottom: 2px; font-size: 14px;">7-DAY CHRONIC STATUS</p>
                            <h2 style="color: {load_color}; margin-top: 0; font-size: 22px;">{load_label}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Styled Alert Banners
                if risk == "HIGH":
                    st.error(f"⚠️ **HIGH RISK DETECTED** (Confidence: {confidence_pct}%) — Immediate tactical relief & medical intervention required!")
                elif risk == "MEDIUM":
                    st.warning(f"⚡ **MEDIUM RISK** (Confidence: {confidence_pct}%) — Monitor sleep patterns and optimize rotational workload.")
                else:
                    st.success(f"✅ **LOW RISK** (Confidence: {confidence_pct}%) — Jawan parameters within safe operating limits.")
            else:
                st.error(f"API Error ({response.status_code}): {response.text}")
                
        except Exception as e:
            st.error(f"Connection failed: Ensure FastAPI server is running (`uvicorn app:app --reload`). Error: {e}")