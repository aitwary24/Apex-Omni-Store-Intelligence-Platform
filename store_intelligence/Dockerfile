FROM python:3.11-slim

# Install system-level OpenCV dependencies (Fixed libgl1 package name)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements from the subfolder
COPY store_intelligence/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from current root to /app inside container
COPY . .

# Adjust for the folder structure inside the container
ENV PYTHONPATH=/app/store_intelligence

EXPOSE 8000
CMD ["uvicorn", "store_intelligence.app.main:app", "--host", "0.0.0.0", "--port", "8000"]