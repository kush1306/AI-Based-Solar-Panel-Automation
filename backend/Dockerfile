# ---- Base Image ----
FROM python:3.11-slim

# ---- Environment setup ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ---- Working directory ----
WORKDIR /app

# ---- System dependencies ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Python dependencies first (better layer caching) ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy application code ----
COPY . .

# ---- Expose FastAPI default port ----
EXPOSE 8000

# ---- Start command ----
# Assumes your FastAPI app instance is named "app" inside main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]