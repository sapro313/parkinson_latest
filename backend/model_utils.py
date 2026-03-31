import pickle
import numpy as np

model = pickle.load(open('parkinson_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
features = pickle.load(open('features.pkl', 'rb'))

def predict(inputs):
    ordered = [inputs[f] for f in features]
    arr = np.array(ordered).reshape(1, -1)

    arr = scaler.transform(arr)

    pred = model.predict(arr)
    prob = model.predict_proba(arr)[0]

    return pred, prob