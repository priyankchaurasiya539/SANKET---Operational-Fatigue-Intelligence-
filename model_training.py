import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 1. Load Dataset
print("Loading data...")
df = pd.read_csv('data/Defence_dataset.csv')

#now convert date to datetime Object to perform various operations (like filtering and sorting easily)
df['date'] = pd.to_datetime(df['date'], format='mixed', dayfirst=True)

# 2. Define Multi-Class Target Variable
def create_risk_category(score):
    if score < 4.0:
        return 'LOW'
    elif score <= 7.0:
        return 'MEDIUM'
    else:
        return 'HIGH'

df['risk_category'] = df['fatigue_score'].apply(create_risk_category)

# 3. Categorical Encoding (One-Hot Encoding)
print("Encoding features...")
categorical_cols = ['force_type', 'role', 'region', 'connectivity_status']
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Convert bool columns to int (0/1) for strict float models
bool_cols = df_encoded.select_dtypes(include='bool').columns
df_encoded[bool_cols] = df_encoded[bool_cols].astype(int)

# 4. Chronological Train-Test Split (70% Train, 30% Test)
split_date = pd.to_datetime('2026-07-21')

train_data = df_encoded[df_encoded['date'] <= split_date]
test_data = df_encoded[df_encoded['date'] > split_date]

# Separate Features (X) and Target (y)
drop_cols = ['personnel_id', 'date', 'fatigue_score', 'risk_category']
X_train = train_data.drop(columns=drop_cols)
y_train = train_data['risk_category']

X_test = test_data.drop(columns=drop_cols)
y_test = test_data['risk_category']

print(f"Training shape: {X_train.shape} | Testing shape: {X_test.shape}")

# 5. Model 1: Logistic Regression Baseline
print("Training Logistic Regression...")
log_reg = LogisticRegression(
    max_iter=1000
)
log_reg.fit(X_train, y_train)
y_pred_lr = log_reg.predict(X_test)

print("\n=== LOGISTIC REGRESSION PERFORMANCE ===")
print(classification_report(y_test, y_pred_lr))

# 6. Model 2: Random Forest Classifier with Balanced Weights
print("Training Random Forest...")
rf_classifier = RandomForestClassifier(
    n_estimators=100, 
    max_depth=8, 
    class_weight='balanced', #It will handle the high risk class (which is low in number) more accurately 
    random_state=42, 
    n_jobs=-1
)
rf_classifier.fit(X_train, y_train)
y_pred_rf = rf_classifier.predict(X_test)

print("\n=== RANDOM FOREST PERFORMANCE ===")
print(classification_report(y_test, y_pred_rf))

#Save the randome forest classifier
joblib.dump(rf_classifier, 'models/rf_model.pkl')

# Save the feature columns so FastAPI knows what columns to expect
joblib.dump(X_train.columns.tolist(), 'models/model_features.pkl')
print("Model and features saved successfully!")

import pandas as pd

# Check feature importances
importances = rf_classifier.feature_importances_
feature_names = X_train.columns

for feature, score in sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True):
    print(f"{feature}: {score:.4f}")