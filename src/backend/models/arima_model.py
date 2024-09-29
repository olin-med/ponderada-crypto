import pandas as pd
import os
import pickle
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler

MODEL_PATH = '/app/models/arima_model.pkl'
SCALER_PATH = '/app/models/scaler.pkl'

def load_data():
    # Caminho absoluto para o arquivo CSV
    data_path = '/app/data/collected_data.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Arquivo {data_path} não encontrado.")
    data = pd.read_csv(data_path)
    return data[['Close']].values.flatten()

def normalize_data(data):
    scaler = MinMaxScaler()
    data_normalized = scaler.fit_transform(data.reshape(-1, 1)).flatten()
    return data_normalized, scaler

def analyze_data():
    data = load_data()
    
    # Plotar ACF e PACF para analisar padrões temporais
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.subplot(211)
    plot_acf(data, ax=plt.gca(), lags=40)
    plt.subplot(212)
    plot_pacf(data, ax=plt.gca(), lags=40)
    plt.show()

def train_arima_model():
    data = load_data()
    data_normalized, scaler = normalize_data(data)

    # Treinar o modelo ARIMA
    model = ARIMA(data_normalized, order=(5, 1, 0))  # Ajuste os parâmetros conforme necessário
    model_fit = model.fit()

    # Salvar o modelo e o scaler
    model_fit.save(MODEL_PATH)
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)

def get_arima_prediction():
    from statsmodels.tsa.arima.model import ARIMAResults

    if not os.path.exists(MODEL_PATH):
        train_arima_model()

    # Carregar o modelo e o scaler
    model_fit = ARIMAResults.load(MODEL_PATH)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)

    # Fazer a previsão para o próximo período
    normalized_prediction = model_fit.forecast(steps=1)[0]
    prediction = scaler.inverse_transform([[normalized_prediction]])[0][0]
    
    return prediction
