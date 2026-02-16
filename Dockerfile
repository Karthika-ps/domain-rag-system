FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first (for Docker layer caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ ./src/
COPY vector_store/ ./vector_store/
COPY data/ ./data/

EXPOSE 5000

CMD ["python", "src/app.py"]
