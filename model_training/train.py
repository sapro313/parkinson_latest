import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# ✅ FIXED LOADING
df_raw = pd.read_csv('../dataset/parkinsons.csv')

# Split single column into proper columns
column_names = df_raw.columns[0].split(',')
df = df_raw.iloc[:, 0].str.split(',', expand=True)
df.columns = column_names

# Convert numeric columns
for col in df.columns:
    if col != 'name':
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.drop(columns=['name'], errors='ignore')
df = df.dropna()

# ✅ NOW THIS WILL WORK
X = df.drop(columns=['status'])
y = df['status'].astype(int)

features = X.columns.tolist()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train_scaled, y_train)

print("Accuracy:", model.score(X_test_scaled, y_test))

# Save files
pickle.dump(model, open('../backend/parkinson_model.pkl', 'wb'))
pickle.dump(scaler, open('../backend/scaler.pkl', 'wb'))
pickle.dump(features, open('../backend/features.pkl', 'wb'))

print("✅ Training complete")