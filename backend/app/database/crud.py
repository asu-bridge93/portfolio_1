# データベースのCRUD操作を行う関数を定義する

from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from . import models

def save_prediction(db: Session, input_data: Dict[str, float], prediction_result: Dict[str, Any]) -> models.Prediction:
    """予測結果をデータベースに保存する"""
    # Args: db: データベースsession, input_data: 入力特徴量, prediction_result: 予測結果
    # input_data: 特徴量の辞書（特徴量名、数値）
    # prediction_result: 予測結果の辞書（予測結果、信頼度）
    # Returns: 保存された予測結果のデータベースエントリ

    db_prediction = models.Prediction(
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

def get_prediction_history(db: Session, skip: int = 0, limit: int = 100) -> List[models.Prediction]:
    """予測履歴をデータベースから取得する"""
    # Args: db: データベースsession, skip: 何番目のエントリから取得するか, limit: 取得するレコードの最大数
    # Returns: 予測履歴のリスト

    return db.query(models.Prediction).order_by(models.Prediction.timestamp.desc()).offset(skip).limit(limit).all()

def get_prediction_by_id(db: Session, prediction_id: int) -> Optional[models.Prediction]:
    """IDで予測結果をデータベースから取得する"""
    # Args: db: データベースsession, prediction_id: 予測結果のID
    # Returns: 予測結果
    return db.query(models.Prediction).filter(models.Prediction.id == prediction_id).first()
