# Use the official Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Ensure that python outputs go straight to the terminal
ENV PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies needed for psycopg2 (Neon DB) and others
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Make the entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Set the PORT environment variable if not already set (Cloud Run uses 8080 by default)
ENV PORT=8080

# Run the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
