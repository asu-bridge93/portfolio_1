from pydantic import BaseModel, Field
# Pydantic は データの型チェック や バリデーション（データの正しさを確認） をしてくれる Python のライブラリ
# API のリクエストやレスポンスのデータが正しい形になっているか確認するために使う
from typing import List, Optional, Dict, Any
from datetime import datetime

class PredictionRequest(BaseModel):
    """予測リクエストのスキーマ"""
    sepal_length: float = Field(..., description="がく片の長さ(cm)")
    sepal_width: float = Field(..., description="がく片の幅(cm)")
    petal_length: float = Field(..., description="花弁の長さ(cm)")
    petal_width: float = Field(..., description="花弁の幅(cm)")

    class Config:
        schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }

class PredictionResponse(BaseModel):
    """予測結果のスキーマ"""
    id: int
    timestamp: datetime
    input_data: Dict[str, float]
    prediction: str
    prediction_id: int
    confidence: float
    probabilities: Dict[str, float]

    class Config:
        orm_mode = True
    # SQLAlchemy のモデルを Pydantic モデルに変換できるようにする

class PredictionList(BaseModel):
    """予測履歴のリスト"""
    total: int
    predictions: List[PredictionResponse]

class HealthCheckResponse(BaseModel):
    """ヘルスチェックのレスポンス"""
    status: str
    version: str