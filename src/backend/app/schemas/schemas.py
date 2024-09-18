# backend/app/schemas/schemas.py

from pydantic import BaseModel
from datetime import datetime

class PriceDataBase(BaseModel):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

class PriceDataCreate(PriceDataBase):
    pass

class PriceData(PriceDataBase):
    id: int

    class Config:
        orm_mode = True

class LogBase(BaseModel):
    action: str
    details: str

class LogCreate(LogBase):
    pass

class Log(LogBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
