# backend/app/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import db_models
from .schemas import schemas
from .crud import crud
from .models import lstm_model, gru_model
# Importar a função de retreinamento
from .models.retrain import retrain_models

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/prices/", response_model=list[schemas.PriceData])
def read_price_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prices = crud.get_price_data(db, skip=skip, limit=limit)
    return prices

@app.get("/predict/lstm")
def predict_lstm(db: Session = Depends(get_db)):
    prediction = lstm_model.get_lstm_prediction()
    crud.log_action(db, "LSTM Prediction", "Prediction made using LSTM model.")
    return {"prediction": prediction}

@app.get("/predict/gru")
def predict_gru(db: Session = Depends(get_db)):
    prediction = gru_model.get_gru_prediction()
    crud.log_action(db, "GRU Prediction", "Prediction made using GRU model.")
    return {"prediction": prediction}

@app.post("/retrain")
def retrain_models_endpoint(db: Session = Depends(get_db)):
    retrain_models()
    crud.log_action(db, "Retrain Models", "Models retrained successfully.")
    return {"message": "Models retrained successfully"}
