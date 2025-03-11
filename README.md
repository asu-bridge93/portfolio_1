# Loan Default Prediction API

A production-ready machine learning microservice that predicts loan default risk, built with FastAPI, containerization, CI/CD, and cloud deployment.

## [Live Demo(not available now)]()

## Project Overview

This project showcases a comprehensive MLOps implementation for loan default risk assessment:

- **End-to-end ML pipeline** from model training through production deployment
- **Real-time prediction API** with robust error handling and input validation
- **Complete DevOps integration** with containerization and automated deployment
- **Industry best practices** in ML engineering and software development

The service analyzes loan application data to predict default probability, helping financial institutions better manage risk while demonstrating advanced software engineering principles.

## Key Features

- **ML-powered risk assessment** using scikit-learn models trained on loan data
- **High-performance API** built with FastAPI for low-latency predictions
- **Persistent storage** with SQLAlchemy ORM for prediction history and model tracking
- **Cloud-native architecture** with Docker containerization
- **Automated CI/CD pipeline** using GitHub Actions for seamless deployment
- **Interactive API documentation** with Swagger UI

## Technical Stack

| Component | Technology |
|-----------|------------|
| ML Framework | scikit-learn |
| API | FastAPI |
| Database | SQLAlchemy ORM |
| Containerization | Docker |
| CI/CD | GitHub Actions |
| Cloud Platform | Google Cloud Run |
| Package Management | uv (high-performance Python package installer) |

## Project Structure

```
backend/
├── Dockerfile                # Docker container configuration
├── app                       # Main application directory
│   ├── api
│   │   └── api_schemas.py    # Pydantic schemas for API validation
│   ├── database              # Database components
│   │   ├── crud.py           # Database operations
│   │   ├── database.py       # DB connection setup
│   │   └── table.py          # SQLAlchemy models
│   ├── main.py               # FastAPI entry point
│   └── model
│       └── wrapper.py        # ML model interface
├── model_training            # Model development
│   ├── data
│   │   └── Loan_default.csv  # Training dataset
│   ├── experiment-notebook.ipynb  # Experimentation notebook
│   └── train.py              # Model training script
└── requirements.txt          # Project dependencies
```

## Data Source

This project uses the [Loan Default Dataset from Kaggle](https://www.kaggle.com/datasets/nikhil1e9/loan-default) for model training and validation.

## Getting Started

### Quick Setup with uv

[uv](https://github.com/astral-sh/uv) provides significantly faster dependency resolution and installation:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
iwr -useb https://astral.sh/uv/install.ps1 | iex # Windows

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -r requirements.txt
```

### Local Development

```bash
# Train the model
python model_training/train.py

# Start the application
uvicorn app.main:app --reload
```

Access the API documentation at http://localhost:8000/docs

### Docker Deployment

```bash
# Build the image
docker build -t backend .

# Run the container
docker run -p 8000:8000 backend
```

## CI/CD Pipeline

The project implements a streamlined CI/CD workflow with GitHub Actions:

1. Code push to GitHub repository
2. Automated Docker image building
3. Deployment to Google Cloud Run

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict` | POST | Submit loan data and receive default prediction |
| `/history` | GET | Retrieve recent prediction records from database |
| `/history_id` | GET | Get specific prediction record by ID |
| `/health` | GET | System health check for monitoring |

## Future Development

- Enhanced feature engineering to improve model performance
- Frontend visualization dashboard for prediction insights

## License

MIT

---

© 2025 | [GitHub Profile](https://github.com/asu-bridge93)