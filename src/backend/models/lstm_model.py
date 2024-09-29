import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import yfinance as yf
import datetime

# Function to fetch data directly from yfinance
def load_data():
    # Define the date range
    start_date = '2020-01-01'
    end_date = datetime.date.today().strftime('%Y-%m-%d')
    
    # Fetch data from yfinance
    data_df = yf.download('BTC-USD', start=start_date, end=end_date, interval='1d')
    if data_df.empty:
        raise ValueError("No data fetched from yfinance. Please check the ticker symbol and date range.")
    
    # Reset index to make 'Date' a column
    data_df = data_df.dropna().reset_index()
    return data_df[['Date', 'Close']]

data_df = load_data()

# Convert 'Date' to datetime and sort
data_df['Date'] = pd.to_datetime(data_df['Date'])
data_df = data_df.sort_values('Date')

# Reset index after sorting
data_df = data_df.reset_index(drop=True)

# Extract closing prices as numpy array
prices = data_df['Close'].values.reshape(-1, 1)

# Feature Scaling
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_prices = scaler.fit_transform(prices)

# Parameters
SEQ_LENGTH = 60  # Increase sequence length for better context
BATCH_SIZE = 64
EPOCHS = 100
LEARNING_RATE = 0.001

def create_sequences(data, seq_length):
    sequences = []
    targets = []
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i+seq_length])
        targets.append(data[i+seq_length])
    return np.array(sequences), np.array(targets)

# Create sequences
X, y = create_sequences(scaled_prices, SEQ_LENGTH)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# Convert to PyTorch tensors
X_train = torch.from_numpy(X_train).float()
y_train = torch.from_numpy(y_train).float()
X_test = torch.from_numpy(X_test).float()
y_test = torch.from_numpy(y_test).float()

class LSTMModel(nn.Module):
    def __init__(self, input_size=1, hidden_size=50, num_layers=2):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.lstm = nn.LSTM(
            input_size, hidden_size, num_layers, batch_first=True, dropout=0.2
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        h0 = torch.zeros(
            self.num_layers, x.size(0), self.hidden_size
        ).requires_grad_()
        c0 = torch.zeros(
            self.num_layers, x.size(0), self.hidden_size
        ).requires_grad_()

        out, _ = self.lstm(x, (h0.detach(), c0.detach()))
        out = self.fc(out[:, -1, :])
        return out

def train_model(model, X_train, y_train, epochs=EPOCHS, lr=LEARNING_RATE):
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    model.train()

    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()

        if (epoch+1) % 10 == 0:
            print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.6f}')

    return model

def evaluate_model(model, X_test, y_test):
    model.eval()
    with torch.no_grad():
        predicted = model(X_test).numpy()
    # Inverse transform to get actual prices
    predicted = scaler.inverse_transform(predicted)
    actual = scaler.inverse_transform(y_test.numpy())

    return predicted, actual

def predict_future(model, days=5):
    model.eval()
    last_sequence = X_test[-1].unsqueeze(0)  # Use last sequence from test data
    predictions = []

    with torch.no_grad():
        for _ in range(days):
            out = model(last_sequence)
            predictions.append(out.item())

            # Prepare next input sequence
            out_scaled = torch.tensor(out.item()).reshape(1, 1, 1)
            last_sequence = torch.cat((last_sequence[:, 1:, :], out_scaled), dim=1)

    # Inverse transform predictions
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
    return predictions


trained_model = None  # Global variable to hold the trained model

def trigger_training():
    global trained_model
    model = LSTMModel()
    print("Training started...")
    trained_model = train_model(model, X_train, y_train)
    print("Training completed.")
    return {"message": "Model trained successfully"}

def trigger_prediction(days=5):
    if trained_model is None:
        return {"error": "Model has not been trained yet."}

    future_predictions = predict_future(trained_model, days)

    # Get the historical data for plotting
    historical_prices = scaler.inverse_transform(scaled_prices).flatten().tolist()
    historical_dates = data_df['Date'].dt.strftime('%Y-%m-%d').tolist()

    # Future dates
    last_date = data_df['Date'].iloc[-1]
    future_dates = [(last_date + pd.Timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, days+1)]

    return {
        "prediction": {
            "dates": future_dates,
            "prices": future_predictions.tolist()
        },
        "historical": {
            "dates": historical_dates,
            "prices": historical_prices
        }
    }

