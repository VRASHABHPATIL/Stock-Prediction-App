import numpy as np
from data_collection import preprocess_data

def make_prediction(generator, scaler, last_sequence):
    prediction = generator.predict(last_sequence.reshape(1, -1, 2))
    # Reshape the prediction to 2D before inverse transform
    prediction_2d = prediction.reshape(-1, 2)
    unscaled_prediction = scaler.inverse_transform(prediction_2d)
    return unscaled_prediction[0]

def get_last_sequence(data, seq_length):
    scaled_data, scaler = preprocess_data(data)
    return scaled_data[-seq_length:], scaler
