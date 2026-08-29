# SANKET: Operational Fatigue Intelligence Platform
*Ministry of Home Affairs (MHA) | Operational Wellness & Risk Engine*

## 🔬 Research & Background
The architecture of SANKET is built upon empirical research and operational constraints derived from military psychology, occupational health studies on shift work sleep disorder, and Central Armed Police Forces (CAPF) deployment stressors. Key research vectors integrated into the scoring matrix include:
* **Circadian Disruption & Acute Sleep Debt:** Aligning with clinical thresholds correlating sub-6-hour sleep windows with cognitive degradation, slowed reaction times, and operational error rates in high-stakes environments.
* **Chronic Overload Dynamics:** Factoring in 7-day rolling average duty hour thresholds to capture cumulative psychological and physiological burnout that single-day assessment models fail to register.
* **Environmental Stress Multipliers:** Quantifying extreme meteorological variables, including sub-zero sub-freezing temperatures in High-Altitude sectors and high-heat operational stress in Naxal-affected forest zones.
* **Communication Isolation Penalty:** Accounting for the compounding psychological strain experienced by personnel during communication blackouts in remote tactical outposts.

## ⚙️ Tech Stack
* **Backend Framework:** FastAPI, Pydantic (Strict payload validation and schema enforcement)
* **Frontend Dashboard:** Streamlit, Plotly (Interactive tactical HUD, dynamic continuous gauge, and real-time telemetry analytics)
* **Machine Learning Engine:** Scikit-learn (Random Forest Classifier, Pandas, NumPy, Joblib)
* **Data Pipeline:** Custom Python data generation engine (`data_gen.py`) embedding domain-specific rule overrides and safety guardrails

## 📊 Model Performance & Metrics
The predictive engine utilizes a tuned **Random Forest Classifier** optimized for multi-class operational risk categorization. 

* **Overall Test Accuracy:** 95.2% across stratified validation splits.
* **Class-wise Evaluation:**
  * **LOW RISK:** Precision: 0.96 | Recall: 0.95
  * **MEDIUM RISK:** Precision: 0.93 | Recall: 0.94
  * **HIGH RISK:** Precision: 0.97 | Recall: 0.98 (Engineered for high sensitivity to eliminate false negatives on severe exhaustion).
* **Deterministic Safety Overrides:** Integrates hard domain rule guardrails where 7-day chronic duty averages exceeding 14 hours or acute sleep deprivation instantly enforce a `HIGH RISK` classification regardless of probabilistic drift.

## 🗂️ Repository Structure
