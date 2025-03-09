from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from starlette import status
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
    title="Portfolio_1 -- asu-bridge93",
    description="An API service that provides predictions using a machine learning model trained by iris_dataset",
    version="1.0.0"
)

# ルートエンドポイント - APIドキュメントへリダイレクト
@app.get("/", tags=["Home"])
async def root():
    """
    Redirect to the /docs page.
    This is intended to be connected to the frontend in the future.
    """
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)

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
@app.get("/health", response_model=schemas.HealthCheckResponse, tags=["HealthCheck"])
async def health_check():
    """An endpoint to check the system's status"""
    return {
        "status": "healthy",
        "version": app.version
    }

# 予測エンドポイント
@app.post("/predict", response_model=schemas.PredictionResponse, tags=["Prediction"])
async def create_prediction(
    request: schemas.PredictionRequest,
    db: Session = Depends(database.get_db)
):
    """
    Perform predictions using an AI model and save the results in a database.
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
@app.get("/history", response_model=schemas.PredictionList, tags=["History"])
async def read_predictions(
    skip: int = Query(0, ge=0, description="How many records you skip"),
    limit: int = Query(100, ge=1, le=1000, description="The maximum of the record you get"),
    db: Session = Depends(database.get_db)
):
    """
    Retrieve past prediction history.
    """
    predictions = crud.get_prediction_history(db, skip=skip, limit=limit)
    return {
        "total": len(predictions),
        "predictions": predictions
    }

# 特定の予測履歴取得エンドポイント
@app.get("/history/{prediction_id}", response_model=schemas.PredictionResponse, tags=["History (id)"])
async def read_prediction(
    prediction_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Retrieve the prediction history for a specific ID.
    """
    db_prediction = crud.get_prediction_by_id(db, prediction_id=prediction_id)
    if db_prediction is None:
        raise HTTPException(status_code=404, detail=f"予測ID {prediction_id} が見つかりません")
    return db_prediction
