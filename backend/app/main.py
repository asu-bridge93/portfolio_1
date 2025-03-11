from app.database import table
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from starlette import status
from sqlalchemy.orm import Session
import os
import logging
from typing import List

from app.model.wrapper import ModelWrapper
from app.api import api_schemas
from app.database import crud, database

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Loan Default Prediction -- asu-bridge93",
    description="Predicts loan default risk using a machine learning model based on user financial data.",
    version="1.0.0"
)

# Initialize the database when the application starts
@app.on_event("startup")
async def startup():
    # Create database tables
    table.Base.metadata.create_all(bind=database.engine)
    logger.info("Database initialization completed.")
    
    # Load the machine learning model
    global model
    try:
        model = ModelWrapper()
        logger.info("Model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load the model: {e}")
        if os.getenv("ENVIRONMENT") == "production":
            raise

# Prediction endpoint
@app.post("/predict", response_model=api_schemas.PredictionResponse, tags=["Prediction"])
async def create_prediction(
    request: api_schemas.PredictionRequest,
    db: Session = Depends(database.get_db)
):
    """
    Endpoint for predicting loan default risk using a machine learning model.

    ## Overview
    - Accepts applicant's financial details as input and predicts loan default risk.
    - The prediction result is stored in the database.

    ## Input
    - `PredictionRequest`: Contains applicant information such as age, income, credit score, and loan amount.

    ## Process Flow
    1. Convert request data into a dictionary format.
    2. Run the prediction model.
    3. Save the prediction result to the database.
    4. Return the prediction result as a response.

    ## Output
    - `PredictionResponse`: Includes prediction results (Default or No Default) and probability scores.

    ## Error Handling
    - Returns `500 Internal Server Error` in case of processing failures.
    """
    try:
        input_data = request.dict()
        prediction_result = model.predict(input_data)
        db_prediction = crud.save_prediction(db, input_data, prediction_result)
        return db_prediction
    except Exception as e:
        logger.error(f"Error during prediction processing: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction processing failed: {str(e)}")

# Retrieve prediction history
@app.get("/history", response_model=api_schemas.PredictionList, tags=["History"])
async def read_predictions(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to retrieve"),
    db: Session = Depends(database.get_db)
):
    """
    Retrieve past prediction results with pagination support.

    ## Overview
    - Fetches previously executed loan default predictions.
    - Supports pagination using `skip` and `limit` parameters.

    ## Output
    - `total` (int): Total number of retrieved predictions.
    - `predictions` (list): List of predictions, including input data and results.
    """
    predictions = crud.get_prediction_history(db, skip=skip, limit=limit)
    return {"total": len(predictions), "predictions": predictions}

# Retrieve a specific prediction by ID
@app.get("/history/{prediction_id}", response_model=api_schemas.PredictionResponse, tags=["History_id"])
async def read_prediction(
    prediction_id: int,
    db: Session = Depends(database.get_db)
):
    """
    Retrieve prediction details for a specific ID.
    """
    db_prediction = crud.get_prediction_by_id(db, prediction_id=prediction_id)
    if db_prediction is None:
        raise HTTPException(status_code=404, detail=f"Prediction ID {prediction_id} not found")
    return db_prediction

# Root endpoint - Redirect to API documentation
@app.get("/", tags=["Root"])
async def root():
    """
    Redirects to FastAPI's documentation page (`/docs`).
    """
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)

# ヘルスチェックエンドポイント
@app.get("/health", response_model=api_schemas.HealthCheckResponse, tags=["HealthCheck"])
async def health_check():
    """An endpoint to check the system's status"""
    return {
        "status": "healthy",
        "version": app.version
    }
