# backend/app/models/retrain.py

from .lstm_model import train_lstm_model
from .gru_model import train_gru_model

def retrain_models():
    train_lstm_model()
    train_gru_model()
