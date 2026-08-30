# Dockerfile for FastAPI Backend
FROM python:3.9-slim

# Install Node.js for the JavaScript code sandbox
RUN apt-get update && apt-get install -y nodejs npm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
