from pydantic import BaseModel, Field
# Pydantic は データの型チェック や バリデーション（データの正しさを確認） をしてくれる Python のライブラリ
# API のリクエストやレスポンスのデータが正しい形になっているか確認するために使う
from typing import List, Optional, Dict, Any
from datetime import datetime

class PredictionRequest(BaseModel):
    Age: int = Field(..., description="年齢")
    Income: int = Field(..., description="収入")
    LoanAmount: int = Field(..., description="ローンの金額")
    CreditScore: int = Field(..., description="信用スコア")
    MonthsEmployed: int = Field(..., description="勤続年数")
    NumCreditLines: int = Field(..., description="信用取引数")
    InterestRate: float = Field(..., description="金利")
    LoanTerm: int = Field(..., description="ローンの期間")
    DTIRatio: float = Field(..., description="DTI比率")
    Education: int = Field(..., description="教育")
    EmploymentType: int = Field(..., description="雇用形態")
    MaritalStatus: int = Field(..., description="配偶者の有無")
    HasMortgage: int = Field(..., description="住宅ローンの有無")
    HasDependents: int = Field(..., description="扶養家族の有無")
    LoanPurpose: int = Field(..., description="ローンの目的")
    HasCoSigner: int = Field(..., description="共同署名者の有無")

    class Config:
        schema_extra = {
            "example": {
                "Age": 35,
                "Income": 55000,
                "LoanAmount": 150000,
                "CreditScore": 720,
                "MonthsEmployed": 60,
                "NumCreditLines": 4,
                "InterestRate": 3.5,
                "LoanTerm": 30,
                "DTIRatio": 0.35,
                "Education": 2,
                "EmploymentType": 1,
                "MaritalStatus": 1,
                "HasMortgage": 1,
                "HasDependents": 0,
                "LoanPurpose": 0,
                "HasCoSigner": 0
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