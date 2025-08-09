# Use Python 3.12 slim base image
FROM python:3.12-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Cython
RUN pip install --upgrade pip
RUN pip install cython>=3.0.11

# Set environment variables for compilation
ENV CXXFLAGS="-std=c++11"
ENV CFLAGS="-std=c99"

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --prefer-binary -r requirements.txt

# Copy the entire application code (including app/ and routers/)
COPY . .

# Debug: List files in the working directory (optional, remove after confirmation)
RUN ls -la /app

# Command for FastAPI with correct module path
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]