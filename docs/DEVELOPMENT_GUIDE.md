# RankScope — Developer & Setup Guide

This guide walks you through running RankScope locally for development and testing.

---

## 1. Prerequisites
- Python 3.9+
- Node.js 18+ & npm
- Redis (optional for Celery background tasks; mock provider runs synchronously)

---

## 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp ../.env.example .env

# Run FastAPI server
python3 -m uvicorn app.main:app --reload --port 8000
```

FastAPI Swagger documentation will be available at:
`http://localhost:8000/docs`

---

## 3. Running Automated Tests

Run the full Pytest suite:
```bash
cd backend
python3 -m pytest tests/ -v
```

---

## 4. Frontend Setup (Next.js)

```bash
cd frontend
npm install
npm run dev
```

The Next.js dashboard will be served at `http://localhost:3000`.
