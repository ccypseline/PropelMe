# Use an official lightweight Python image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install system deps (optional, adjust as needed)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirement file & install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port Cloud Run will use
ENV PORT=8080

# Start FastAPI with uvicorn (adjust module/path as needed)
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
