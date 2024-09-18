# scripts/data_collection.py

import yfinance as yf
import pandas as pd

def collect_data(ticker_symbol='BTC-USD', start_date='2020-01-01', end_date='2023-09-01'):
    # Baixar os dados do criptoativo
    data = yf.download(ticker_symbol, start=start_date, end=end_date, interval='1d')
    
    # Resetar o índice e remover valores nulos
    data = data.dropna().reset_index()
    
    # Salvar os dados em um arquivo CSV
    data.to_csv('backend/data/collected_data.csv', index=False)
    
    return data

if __name__ == "__main__":
    collect_data()
