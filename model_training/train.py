import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, RocCurveDisplay, PrecisionRecallDisplay
)
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df_raw = pd.read_csv('../dataset/parkinsons.csv')
column_names = df_raw.columns[0].split(',')
df = df_raw.iloc[:, 0].str.split(',', expand=True)
df.columns = column_names

for col in df.columns:
    if col != 'name':
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.drop(columns=['name'], errors='ignore').dropna()

X = df.drop(columns=['status'])
y = df['status'].astype(int)
features = X.columns.tolist()

# Split and scale
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train_scaled, y_train)

# Predictions
y_pred = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

# Evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_proba)

print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-score: {f1:.4f}")
print(f"ROC-AUC: {roc_auc:.4f}")

# Save model, scaler, features
pickle.dump(model, open('../backend/parkinson_model.pkl', 'wb'))
pickle.dump(scaler, open('../backend/scaler.pkl', 'wb'))
pickle.dump(features, open('../backend/features.pkl', 'wb'))
print("Training complete")

# --------------------------
# Confusion Matrix
# --------------------------
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(5,4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=[0,1], yticklabels=[0,1])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# --------------------------
# ROC Curve
# --------------------------
RocCurveDisplay.from_predictions(y_test, y_proba)
plt.title('ROC Curve')
plt.show()

# --------------------------
# Precision-Recall Curve
# --------------------------
PrecisionRecallDisplay.from_predictions(y_test, y_proba)
plt.title('Precision-Recall Curve')
plt.show()