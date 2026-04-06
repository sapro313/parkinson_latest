import pandas as pd
import pickle
import os
import numpy as np

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'dataset', 'parkinsons.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'backend', 'parkinson_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'backend', 'scaler.pkl')
FEATURES_PATH = os.path.join(BASE_DIR, 'backend', 'features.pkl')

# Load model, scaler, features
model = pickle.load(open(MODEL_PATH, 'rb'))
scaler = pickle.load(open(SCALER_PATH, 'rb'))
features = pickle.load(open(FEATURES_PATH, 'rb'))

print("✅ Model, scaler, and features loaded successfully.")

# Load CSV dataset
df_raw = pd.read_csv(CSV_PATH)
column_names = df_raw.columns[0].split(',')
df = df_raw.iloc[:, 0].str.split(',', expand=True)
df.columns = column_names

for col in df.columns:
    if col != 'name':
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.drop(columns=['name'], errors='ignore').dropna()

X = df.drop(columns=['status'])
y = df['status'].astype(int).values

print(f"✅ Loaded {len(X)} samples from CSV dataset.\n")

# Input validation function
def validate_input(data):
    if not isinstance(data, (pd.DataFrame, pd.Series, list, np.ndarray)):
        return False
    if len(data) != len(features):
        return False
    if any(x is None for x in data):
        return False
    return True

# Test first 5 rows from CSV for input validation and prediction
print("--- Manual Unit Tests on CSV Data ---")
for i in range(5):
    sample_input = X.iloc[i]  # pandas Series with feature names
    valid = validate_input(sample_input)
    
    # Convert to DataFrame with column names (1 row)
    sample_df = pd.DataFrame([sample_input], columns=features)
    
    scaled_input = scaler.transform(sample_df)
    prediction = model.predict(scaled_input)
    proba = model.predict_proba(scaled_input)
    
    print(f"\nSample {i+1}:")
    print(f"Input valid: {valid}")
    print(f"Prediction: {prediction[0]}")
    print(f"Prediction probabilities: {proba[0]}")
    print(f"Actual label: {y[i]}")