FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -v -r requirements.txt

# Copy application code
COPY app/ .

# Create documents directory
RUN mkdir -p /app/documents

# Run the application
CMD ["python", "main.py"] 