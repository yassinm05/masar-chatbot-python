# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install system dependencies (FFmpeg is required for pydub/audio)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (Render sets the PORT env var automatically)
ENV PORT=5000
EXPOSE 5000

# Command to run the app using Gunicorn
# This binds to 0.0.0.0 on the port provided by the environment
CMD gunicorn --bind 0.0.0.0:$PORT app:app