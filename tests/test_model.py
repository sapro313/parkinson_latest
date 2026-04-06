import pickle
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, 'backend', 'parkinson_model.pkl'), 'rb'))
scaler = pickle.load(open(os.path.join(BASE_DIR, 'backend', 'scaler.pkl'), 'rb'))
features = pickle.load(open(os.path.join(BASE_DIR, 'backend', 'features.pkl'), 'rb'))

def test_model_prediction_shape():
    sample_input = np.random.rand(1, len(features))
    sample_scaled = scaler.transform(sample_input)
    prediction = model.predict(sample_scaled)
    assert prediction.shape == (1,)

def test_model_prediction_range():
    sample_input = np.random.rand(1, len(features))
    sample_scaled = scaler.transform(sample_input)
    prediction = model.predict(sample_scaled)
    assert prediction[0] in [0, 1]