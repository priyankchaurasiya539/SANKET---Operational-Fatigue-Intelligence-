import pandas as pd
import numpy as np

np.random.seed(42)
num_personnel = 3334 
days = 30

personnel_ids = [f"P{str(i).zfill(4)}" for i in range(1, num_personnel + 1)]

forces = ['BSF', 'CRPF', 'ITBP', 'CISF', 'SSB', 'Assam_Rifles']
assigned_forces = np.random.choice(forces, size=num_personnel, p=[0.25, 0.30, 0.10, 0.20, 0.05, 0.10])
assigned_roles = np.random.choice(['GD_Patrol', 'QRT_SpecialOps', 'Support_Tech'], size=num_personnel, p=[0.60, 0.10, 0.30])

def assign_region(force):
    if force == 'ITBP': return 'High_Altitude'
    if force == 'Assam_Rifles': return 'Northeast_Forest'
    if force == 'CISF': return np.random.choice(['Urban_Plains', 'Industrial_Belt'])
    if force == 'BSF': return np.random.choice(['Desert', 'Plains', 'High_Altitude'], p=[0.4, 0.4, 0.2])
    if force == 'CRPF': return np.random.choice(['Naxal_Forest', 'Urban_Plains', 'High_Altitude'], p=[0.5, 0.3, 0.2])
    if force == 'SSB': return 'Forest_Foothills'

df_personnel = pd.DataFrame({
    'personnel_id': personnel_ids,
    'force_type': assigned_forces,
    'role': assigned_roles,
    'region': [assign_region(f) for f in assigned_forces],
    'service_years': np.random.randint(1, 30, num_personnel)
})

dates = pd.date_range(start='2026-07-01', periods=days)
df_logs = pd.MultiIndex.from_product([personnel_ids, dates], names=['personnel_id', 'date']).to_frame(index=False)
df_master = df_logs.merge(df_personnel, on='personnel_id', how='left')

n_logs = len(df_master)
base_duty = np.random.normal(9, 1.5, n_logs)
df_master['duty_hours'] = np.where(df_master['role'] == 'GD_Patrol', base_duty + 2, base_duty).clip(6, 24)
df_master['temperature_c'] = np.where(df_master['region'] == 'High_Altitude', np.random.normal(-5, 8, n_logs), np.random.normal(30, 5, n_logs))
df_master['sleep_duration'] = np.round(np.random.normal(7.5, 1.2, n_logs) - (df_master['duty_hours'] > 12).astype(float), 1).clip(2, 10)
df_master['connectivity_status'] = np.where(df_master['region'].isin(['High_Altitude', 'Naxal_Forest']), np.random.choice(['Blackout', 'Full'], p=[0.5, 0.5], size=n_logs), 'Full')

# 1. Pehle rolling average calculate karo taaki column pehle exist kare
df_master = df_master.sort_values(by=['personnel_id', 'date']).reset_index(drop=True)
df_master['7d_avg_duty'] = np.round(df_master.groupby('personnel_id')['duty_hours'].transform(lambda x: x.rolling(7, min_periods=1).mean()), 1)

# 2. Ab '7d_avg_duty' available hai, toh penalty aur raw_fatigue calculate karo
chronic_penalty = np.where(df_master['7d_avg_duty'] > 12, (df_master['7d_avg_duty'] - 10) * 1.5, 0)

raw_fatigue = (
    (df_master['duty_hours'] / 2.5) + 
    ((7.5 - df_master['sleep_duration']).clip(0, 5) * 1.2) + 
    chronic_penalty + 
    (df_master['connectivity_status'] == 'Blackout').astype(float)
)
df_master['fatigue_score'] = np.round(raw_fatigue, 1).clip(1, 10)

def assign_risk(score):
    if score >= 7.0:
        return 'HIGH'
    elif score >= 4.5:
        return 'MEDIUM'
    else:
        return 'LOW'

df_master['risk_category'] = df_master['fatigue_score'].apply(assign_risk)

df_master.to_csv('data/Defence_dataset.csv', index=False)
print(f"Dataset generated successfully with {len(df_master)} rows.")