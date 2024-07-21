import os
import numpy as np
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import LSTM, Dense, Input, Reshape
from tensorflow.keras.optimizers import Adam
import tensorflow as tf

def build_gan(seq_length, features):
    # Generator
    generator = Sequential([
        Input(shape=(seq_length, features)),
        LSTM(64, return_sequences=True),
        LSTM(32, return_sequences=False),
        Dense(features),
        Reshape((1, features))
    ], name='generator')
    
    # Discriminator
    discriminator = Sequential([
        Input(shape=(seq_length, features)),
        LSTM(64, return_sequences=True),
        LSTM(32, return_sequences=False),
        Dense(1, activation='sigmoid')
    ], name='discriminator')
    
    # GAN
    gan_input = Input(shape=(seq_length, features))
    gen_output = generator(gan_input)
    gan_output = discriminator(tf.keras.layers.Concatenate(axis=1)([gan_input[:, 1:, :], gen_output]))
    gan = Model(gan_input, gan_output, name='gan')
    
    return generator, discriminator, gan

def train_gan(generator, discriminator, gan, X_train, y_train, epochs=100, batch_size=32):
    for epoch in range(epochs):
        idx = np.random.randint(0, X_train.shape[0], batch_size)
        real_seq = X_train[idx]
        real_next = y_train[idx]
        
        gen_input = real_seq
        fake_next = generator.predict(gen_input)
        
        real_data = np.concatenate([real_seq[:, 1:, :], real_next.reshape(-1, 1, 2)], axis=1)
        fake_data = np.concatenate([real_seq[:, 1:, :], fake_next], axis=1)
        
        d_loss_real = discriminator.train_on_batch(real_data, np.ones((batch_size, 1)))
        d_loss_fake = discriminator.train_on_batch(fake_data, np.zeros((batch_size, 1)))
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
        
        g_loss = gan.train_on_batch(gen_input, np.ones((batch_size, 1)))
        
        if epoch % 10 == 0:
            print(f"Epoch {epoch}, D Loss: {d_loss}, G Loss: {g_loss}")

    return generator
def save_model(generator, filename):
    generator.save_weights(filename)
    
def load_model(filename):
    # Instead of loading the model, we'll rebuild it
    seq_length = 60  # This should match your original sequence length
    features = 2  # This should match your original number of features
    
    model = Sequential([
        Input(shape=(seq_length, features)),
        LSTM(64, return_sequences=True),
        LSTM(32, return_sequences=False),
        Dense(features),
        Reshape((1, features))
    ], name='generator')
    
    # If the file exists, load the weights
    if os.path.exists(filename):
        model.load_weights(filename)
    
    return model
