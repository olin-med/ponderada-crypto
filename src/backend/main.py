from fastapi import FastAPI, Request
from models import lstm_model, arima_model
from scripts import data_collection
import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # This allows all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # This allows all headers
)

# Variável global para armazenar o modelo treinado
trained_model = None
# Simulated log storage
logs = []

@app.get("/")
def read_root():
    return {"message": "API is running"}



# Rota para treinar o modelo LSTM
@app.post("/train/")
def train_lstm():
    data_collection.collect_data()
    result = lstm_model.trigger_training()
    return result

# Route to make predictions using the trained model
@app.get("/predict/")
def predict(days: int = 5):
    result = lstm_model.trigger_prediction(days)
    return result

# Logging endpoint
@app.post("/log")
async def log_action(request: Request):
    data = await request.json()
    action = data.get("action")
    timestamp = datetime.datetime.now()
    logs.append({"action": action, "timestamp": timestamp})
    print(f"Logged: {action} at {timestamp}")
    return {"message": "Action logged"}
