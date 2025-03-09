# Portfolio: AI Model API

## Overview
This project is an app by Machine Learning model built with FastAPI. 
It includes functionalities for 
- training a machine learning model, 
- managing a database, 
- serving predictions via a RESTful API. 
The project is structured to ensure scalability and maintainability.

## Project Structure
```
backend/
├── app/
│   ├── main.py           # FastAPI entry point
│   ├── models/
│   │   ├── ml_model.py   # Model wrapper for inference
│   │   └── schemas.py    # Pydantic schemas for request/response validation
│   └── database/
│       ├── crud.py       # Database CRUD operations
│       ├── database.py   # Database connection settings
│       └── models.py     # SQLAlchemy ORM models
├── model_training/
│   ├── train.py          # Model training script
│   └── data/
│       └── dataset.csv   # Training dataset
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
[`uv`](https://github.com/astral-sh/uv) is a fast Python package manager that can replace `pip` and `venv`. If you don't have `uv` installed, take it in by the following command.
For macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
iwr -useb https://astral.sh/uv/install.ps1 | iex # Windows
```

After that, run the code bellow.
```bash
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

uv pip install -r requirements.txt
```

### 3. Train the Model
Before running the API, train the machine learning model with the provided dataset.
```bash
python model_training/train.py
```

### 4. Run the Backend Server
Start the FastAPI server with Uvicorn.
```bash
uvicorn app.main:app --reload
```

### 5. Test the API
Open your browser and navigate to Swagger UI: http://localhost:8000/docs to explore and test the API endpoints interactively.

## Features
- **Machine Learning Model**: Train and deploy a model for inference.
- **FastAPI Framework**: Provides high-performance, asynchronous API handling.
- **Database Management**: Uses SQLAlchemy for data persistence.
- **Interactive API Documentation**: Accessible via Swagger UI.

## License
This project is licensed under the MIT License. Feel free to modify and distribute it.

---

### 📌 Author
[Asuka Miyazaki](https://github.com/asu-bridge93)

