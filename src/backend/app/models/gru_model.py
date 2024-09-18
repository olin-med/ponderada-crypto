# backend/app/models/gru_model.py

import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import GRU, Dense
import pandas as pd
import os

MODEL_PATH = 'backend/app/models/gru_model.h5'

def load_data():
    data = pd.read_csv('backend/data/collected_data.csv')
    data = data[['Close']].values
    return data

def prepare_data(data, look_back=60):
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(look_back, len(scaled_data)):
        X.append(scaled_data[i-look_back:i, 0])
        y.append(scaled_data[i, 0])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    return X, y, scaler

def train_gru_model():
    data = load_data()
    X, y, scaler = prepare_data(data)

    # Dividir em treino e teste
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # Construir o modelo
    model = Sequential()
    model.add(GRU(50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(GRU(50))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

    # Salvar o modelo e o scaler
    model.save(MODEL_PATH)
    np.save('backend/app/models/gru_scaler.npy', scaler.scale_)

def get_gru_prediction():
    if not os.path.exists(MODEL_PATH):
        train_gru_model()

    model = load_model(MODEL_PATH)
    scaler_scale = np.load('backend/app/models/gru_scaler.npy')

    data = load_data()
    last_60_days = data[-60:]

    # Preparar os dados
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.scale_ = scaler_scale
    scaled_data = scaler.transform(last_60_days)

    X_input = np.array([scaled_data.flatten()])
    X_input = np.reshape(X_input, (X_input.shape[0], X_input.shape[1], 1))

    # Fazer a previsão
    predicted_price = model.predict(X_input)
    predicted_price = scaler.inverse_transform(predicted_price)

    return predicted_price[0][0]
