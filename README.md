# SANKET: Operational Fatigue Intelligence Platform
*Ministry of Home Affairs (MHA) | Operational Wellness & Risk Engine*

## 🔬 Research & Background
SANKET is designed using studies on military behavior, sleep problems, and real-life stress faced by Central Armed Police Forces (CAPF). The main factors included in its system are:

* **Sleep Problems & Lack of Sleep:** Sleeping less than 6 hours leads to poor concentration, slower reactions, and more mistakes in dangerous situations.
* **Long-Term Burnout:** Tracking work hours over a 7-day period to measure total mental and physical tiredness that checking just a single day would miss.
* **Extreme Weather Stress:** Factoring in harsh weather conditions, such as freezing cold in high mountains or heavy heat in forest deployment zones.
* **Loss of Communication:** Accounting for the extra mental stress when personnel are cut off from communication in remote camps.

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
