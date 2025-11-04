FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Default port (can be overridden with PORT env var)
ENV PORT=5000

# Expose port
EXPOSE ${PORT}

# Run with gunicorn for production
CMD sh -c "gunicorn --bind 0.0.0.0:${PORT} --workers 2 --timeout 60 app:app"
