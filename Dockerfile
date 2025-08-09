FROM python:3.13-slim

# Install build dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Cython first
RUN pip install --upgrade pip
RUN pip install cython>=3.0.10

# Install dependencies from requirements.txt
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefer-binary -r requirements.txt

# Copy application code
COPY . .

# Set environment variables for C++ standard
ENV CXXFLAGS="-std=c++11"

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]