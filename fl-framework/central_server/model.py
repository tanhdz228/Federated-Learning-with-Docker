import numpy as np

def initialize_model():
    return np.zeros(5)

def aggregate_update(updates):
    return np.mean(updates, axis=0)