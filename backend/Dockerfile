# ============================
# FastAPI + Uvicorn + ML Dockerfile
# ============================

FROM python:3.11-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
# - build-essential: for building wheels
# - libpq-dev: PostgreSQL support for psycopg2
# - libglib2.0-0, libsm6, libxrender1, libxext6: required for OpenCV headless
# - libopencv-dev (optional): helps with cv2 linking issues
# - curl: debugging (optional)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libopencv-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (for caching)
COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel

# Install all Python dependencies from your file
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
