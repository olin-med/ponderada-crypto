# backend/app/crud/crud.py

from sqlalchemy.orm import Session
from ..models import db_models
from ..schemas import schemas

def get_price_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.PriceData).offset(skip).limit(limit).all()

def create_price_data(db: Session, price_data: schemas.PriceDataCreate):
    db_price_data = db_models.PriceData(**price_data.dict())
    db.add(db_price_data)
    db.commit()
    db.refresh(db_price_data)
    return db_price_data

def log_action(db: Session, action: str, details: str):
    log_entry = db_models.Log(action=action, details=details)
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry
