from fastapi import FastAPI
import pandas as pd
from datetime import datetime
import os
from model_utils import predict, features

app = FastAPI()

# ✅ CORS (already correct)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ File setup
RESULT_FILE = "parkinson_results.csv"

if not os.path.exists(RESULT_FILE):
    pd.DataFrame(columns=["Timestamp", "Prediction", "Confidence"]).to_csv(RESULT_FILE, index=False)


# 🔐 Login
@app.post("/login")
def login(data: dict):
    if data["username"] == "doctor" and data["password"] == "1234":
        return {"status": "success"}
    return {"status": "fail"}


# 🧠 Predict (UPDATED)
@app.post("/predict")
def predict_api(data: dict):
    pred, prob = predict(data["inputs"])

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if pred[0] == 1:
        result = "Parkinson Detected"
        confidence = float(prob[1])
    else:
        result = "Healthy"
        confidence = float(prob[0])

    # ✅ Save to CSV
    df = pd.read_csv(RESULT_FILE)

    new_row = pd.DataFrame({
        "Timestamp": [timestamp],
        "Prediction": [result],
        "Confidence": [confidence]
    })

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(RESULT_FILE, index=False)

    return {"result": result, "confidence": confidence}


# 📊 HISTORY API (NEW — IMPORTANT)
@app.get("/history")
def get_history():
    df = pd.read_csv(RESULT_FILE)

    # Convert to frontend-friendly format
    formatted = []
    for _, row in df.iterrows():
        formatted.append({
            "timestamp": row["Timestamp"],
            "result": row["Prediction"],
            "confidence": float(row["Confidence"])
        })

    return formatted


# 📊 (OPTIONAL — keep if needed)
@app.get("/results")
def get_results():
    return pd.read_csv(RESULT_FILE).to_dict(orient="records")


# 📥 Feature list
@app.get("/features")
def get_features():
    return features