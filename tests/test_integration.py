import pickle
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, 'backend', 'parkinson_model.pkl'), 'rb'))
scaler = pickle.load(open(os.path.join(BASE_DIR, 'backend', 'scaler.pkl'), 'rb'))
features = pickle.load(open(os.path.join(BASE_DIR, 'backend', 'features.pkl'), 'rb'))

def test_full_pipeline():
    sample_input = np.random.rand(1, len(features))
    scaled = scaler.transform(sample_input)
    prediction = model.predict(scaled)
    proba = model.predict_proba(scaled)
    
    assert prediction.shape == (1,)
    assert 0 <= proba[0][0] <= 1
    assert 0 <= proba[0][1] <= 1