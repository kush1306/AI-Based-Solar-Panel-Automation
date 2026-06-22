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
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Install Python dependencies first (better layer caching) ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy dashboard code ----
COPY . .

# ---- Expose Streamlit's default port ----
EXPOSE 8501

# ---- Start command ----
# Update "app.py" if your main Streamlit file has a different name
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]