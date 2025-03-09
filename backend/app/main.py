from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import os
import logging
from typing import List

from app.models.ml_model import ModelWrapper
from app.models import schemas
from app.database import crud, models, database

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPIアプリケーションの作成
app = FastAPI(
    title="AI予測API",
    description="機械学習モデルを使用した予測を提供するAPIサービス",
    version="1.0.0"
)

# アプリケーション起動時にデータベースの初期化
@app.on_event("startup")
async def startup():
    # データベーステーブルの作成
    models.Base.metadata.create_all(bind=database.engine)
    logger.info("データベースの初期化が完了しました")
    
    # モデルのロード
    global model
    try:
        model = ModelWrapper()
        logger.info("モデルのロードが完了しました")
    except Exception as e:
        logger.error(f"モデルのロードに失敗しました: {e}")
        # 開発環境では例外を再度発生させない
        if os.getenv("ENVIRONMENT") == "production":
            raise

# ヘルスチェックエンドポイント
@app.get("/health", response_model=schemas.HealthCheckResponse, tags=["システム"])
async def health_check():
    """システムの状態を確認するエンドポイント"""
    return {
        "status": "healthy",
        "version": app.version
    }

# 予測エンドポイント
@app.post("/predict", response_model=schemas.PredictionResponse, tags=["予測"])
async def create_prediction(
    request: schemas.PredictionRequest,
    db: Session = Depends(database.get_db)
):
    """
    AIモデルを使用して予測を行い、結果をデータベースに保存する
    """
    try:
        # リクエストデータをモデル用の辞書に変換
        input_data = request.dict()
        
        # モデルによる予測
        prediction_result = model.predict(input_data)
        
        # 予測結果をデータベースに保存
        db_prediction = crud.save_prediction(db, input_data, prediction_result)
        
        return db_prediction
    except Exception as e:
        logger.error(f"予測処理でエラーが発生しました: {e}")
        raise HTTPException(status_code=500, detail=f"予測処理に失敗しました: {str(e)}")

# 予測履歴取得エンドポイント
@app.get("/history", response_model=schemas.PredictionList, tags=["履歴"])
async def read_predictions(
    skip: int = Query(0, ge=0, description="スキップするレコード数"),
    limit: int = Query(100, ge=1, le=1000, description="取得するレコードの最大数"),
    db: Session = Depends(database.get_db)
):
    """
    過去の予測履歴を取得する
    """
    predictions = crud.get_prediction_history(db, skip=skip, limit=limit)
    return {
        "total": len(predictions),
        "predictions": predictions
    }

# 特定の予測履歴取得エンドポイント
@app.get("/history/{prediction_id}", response_model=schemas.PredictionResponse, tags=["履歴"])
async def read_prediction(
    prediction_id: int,
    db: Session = Depends(database.get_db)
):
    """
    特定のIDの予測履歴を取得する
    """
    db_prediction = crud.get_prediction_by_id(db, prediction_id=prediction_id)
    if db_prediction is None:
        raise HTTPException(status_code=404, detail=f"予測ID {prediction_id} が見つかりません")
    return db_prediction
