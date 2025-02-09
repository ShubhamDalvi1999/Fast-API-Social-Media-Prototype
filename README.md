# FastAPI Project

This is a basic FastAPI project template.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application:

```bash
uvicorn main:app --reload
```

The application will be available at http://127.0.0.1:8000

## API Documentation

- Interactive API documentation (Swagger UI): http://127.0.0.1:8000/docs
- Alternative API documentation (ReDoc): http://127.0.0.1:8000/redoc

## Available Endpoints

- `GET /`: Welcome message
- `GET /hello/{name}`: Returns a personalized hello message 