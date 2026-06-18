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
    gfortran \
    libopenblas-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Python dependencies first (better layer caching) ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy model code ----
COPY . .

EXPOSE 8001

# ---- Start command (placeholder) ----
# Update once Member 1/2 finalize whether this runs a training job or serves predictions.
CMD ["python", "train.py"]