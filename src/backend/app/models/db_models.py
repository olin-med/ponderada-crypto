# backend/app/models/db_models.py

from sqlalchemy import Column, Integer, String, Float, DateTime
from ..database.db import Base
import datetime

class PriceData(Base):
    __tablename__ = 'price_data'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    action = Column(String)
    details = Column(String)
