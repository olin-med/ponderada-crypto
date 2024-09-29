# data_collection.py

import yfinance as yf
import pandas as pd
import os

def collect_data(ticker_symbol='BTC-USD', start_date='2023-01-01', end_date='2024-09-20'):
    data = yf.download(ticker_symbol, start=start_date, end=end_date, interval='1d')

    if data.empty:
        print("No data collected. Check if the ticker or dates are correct.")
        return

    data = data.dropna().reset_index()
    data_path = '/app/data/collected_data.csv'
    data.to_csv(data_path, index=False)
    print(f"Data saved to {data_path}")

if __name__ == "__main__":
    collect_data()
