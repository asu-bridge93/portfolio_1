from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Base は「データの設計図を作るための土台」みたいなもの
Base = declarative_base()

class Prediction(Base):
    """予測履歴を格納するテーブル"""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    input_data = Column(JSON)
    prediction = Column(String)
    prediction_id = Column(Integer)
    confidence = Column(Float)
    probabilities = Column(JSON)