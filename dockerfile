# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY Backend /app
COPY Frontend/templates /app/templates
COPY Frontend/static /app/static
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Expose port 8080 (for Flask) and 5000 (for MLflow UI)
EXPOSE 8080 5000

# Start MLflow UI and Flask app
CMD ["bash", "-c", "mlflow ui  & python app.py"]
