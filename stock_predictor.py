from data_collection import get_all_stock_symbols, fetch_stock_data, preprocess_data, create_sequences
from model import build_gan, train_gan, save_model, load_model
from prediction import make_prediction, get_last_sequence
from datetime import datetime, timedelta
import os
import numpy as np
from tensorflow.keras.optimizers import Adam

class StockPredictor:
    def __init__(self):
        self.symbols = get_all_stock_symbols()
        self.models = {}
        self.scalers = {}

    def train_all_models(self):
        for symbol in self.symbols:
            print(f"Training model for {symbol}")
            data = fetch_stock_data(symbol, '2010-01-01', datetime.now().strftime('%Y-%m-%d'))
            scaled_data, scaler = preprocess_data(data)
            
            seq_length = 60
            X, y = create_sequences(scaled_data, seq_length)
            
            generator, discriminator, gan = build_gan(seq_length, scaled_data.shape[1])
            
            discriminator.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.0002, beta_1=0.5))
            gan.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.0002, beta_1=0.5))
            
            trained_generator = train_gan(generator, discriminator, gan, X, y)
            
            model_filename = f'generator_model_{symbol}.h5'
            save_model(trained_generator, model_filename)
            
            self.models[symbol] = trained_generator
            self.scalers[symbol] = scaler

    def load_models(self):
        for symbol in self.symbols:
            model_filename = f'generator_model_{symbol}.h5'
            self.models[symbol] = load_model(model_filename)
            print(f"Model for {symbol} loaded/initialized.")

    def predict_stock(self, symbol, days=15):
        if symbol not in self.models:
            print(f"Model for {symbol} not found. Training now.")
            self.train_all_models()

        end_date = datetime.now()
        start_date = end_date - timedelta(days=100)  # Get 100 days of data for prediction
        data = fetch_stock_data(symbol, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        last_sequence, scaler = get_last_sequence(data, 60)
        
        predictions = []
        current_sequence = last_sequence
        for _ in range(days):
            prediction = make_prediction(self.models[symbol], scaler, current_sequence)
            predictions.append(prediction[0])
            current_sequence = np.roll(current_sequence, -1, axis=0)
            current_sequence[-1] = scaler.transform(prediction.reshape(1, -1))[0]
        
        return predictions, data

stock_predictor = StockPredictor()
