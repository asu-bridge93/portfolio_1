from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from . import table

def save_prediction(db: Session, input_data: Dict[str, float], prediction_result: Dict[str, Any]) -> table.Prediction:
    """予測結果をデータベースに保存する"""
    db_prediction = table.Prediction(
        input_data=input_data,
        prediction=prediction_result['prediction'],
        prediction_id=prediction_result['prediction_id'],
        confidence=prediction_result['confidence'],
        probabilities=prediction_result['probabilities']
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

def get_prediction_history(db: Session, skip: int = 0, limit: int = 100) -> List[table.Prediction]:
    """予測履歴をデータベースから取得する"""
    return db.query(table.Prediction).order_by(table.Prediction.timestamp.desc()).offset(skip).limit(limit).all()

def get_prediction_by_id(db: Session, prediction_id: int) -> Optional[table.Prediction]:
    """IDで予測結果をデータベースから取得する"""
    return db.query(table.Prediction).filter(table.Prediction.id == prediction_id).first()