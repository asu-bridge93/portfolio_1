# Portfolio_1

## Overview
This is a FastAPI-based machine learning app that trains and serves a model using the iris dataset. It provides:
- Model training and inference
- A RESTful API for predictions
- Database management with SQLAlchemy

## Project Structure
```
backend/
├── app/
│   ├── main.py           # FastAPI entry point
│   ├── models/ml_model.py   # Model wrapper for inference
│   ├── models/schemas.py    # Pydantic schemas
│   ├── database/crud.py     # Database operations
│   ├── database/database.py # Database connection
│   └── database/models.py   # ORM models
├── model_training/
│   ├── train.py          # Model training script
│   └── data/dataset.csv  # Training dataset
├── requirements.txt
.gitignore
README.md
```

## Setup
### 1. Clone the Repository
```bash
git clone https://github.com/asu-bridge93/portfolio_1.git
cd backend
```

### 2. Install Dependencies
#### Using `uv` (Recommended)
[`uv`](https://github.com/astral-sh/uv) is a fast Python package manager. Install it with:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
iwr -useb https://astral.sh/uv/install.ps1 | iex # Windows
```
Then, set up a virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
uv pip install -r requirements.txt
```

### 3. Train the Model
```bash
python model_training/train.py
```

### 4. Run the Backend Server
```bash
uvicorn app.main:app --reload
```

### 5. Test the API
Access Swagger UI at: [http://localhost:8000/docs](http://localhost:8000/docs)

## Features
- **FastAPI-based API** for high-performance ML model serving
- **Model training & inference** using the iris dataset
- **Database support** with SQLAlchemy
- **Interactive API documentation** via Swagger UI

## License
MIT License. Free to modify and distribute.

---
### 📌 Author
[asu-bridge93](https://github.com/asu-bridge93)

