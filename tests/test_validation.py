import numpy as np

def validate_input(data):
    if not isinstance(data, (list, np.ndarray)):
        return False
    if len(data) == 0:
        return False
    if any([x is None for x in data]):
        return False
    return True

def test_valid_input():
    data = [0.5, 1.2, 3.4]
    assert validate_input(data) == True

def test_invalid_input_empty():
    data = []
    assert validate_input(data) == False

def test_invalid_input_none():
    data = [0.5, None, 2.3]
    assert validate_input(data) == False

def test_invalid_input_type():
    data = "invalid"
    assert validate_input(data) == False