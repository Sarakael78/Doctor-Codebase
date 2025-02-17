# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies including curl for the healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file from the repository root to leverage layer caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the repository into the container
COPY . /app/

# Expose the port used by Gradio (7860 by default)
EXPOSE 4444

# Optional metadata labels
LABEL Name="DSB-DoctorCodebase" \
      Description="A Python/Gradio tool that concatanates codebases for ingestion into AI Chat Bot." \
      Maintainer="dsbworkaholic@gmail.com" \
      License="MIT" \
      Version="1.0"

# Set environment variables for Gradio
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=4444

# Healthcheck: ensure the service is running properly
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:4444/ || exit 1

# Command to run the application
CMD ["python", "main.py"]