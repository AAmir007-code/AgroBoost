# .dockerignore (to optimize build context and prevent unnecessary files from being copied)
# ------------------------------------
# .git
# __pycache__
# *.py[cod]
# *.pyo
# venv
# tests
# node_modules
# staticfiles
# media

# Stage 1: Builder Stage (Install dependencies)
FROM python:3.10-slim AS builder

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy only requirements first (to cache dependencies better)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --user --no-cache-dir --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final Image (Runtime)
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user for security
RUN useradd -m django_user

# Set work directory
WORKDIR /app

# Copy only the necessary runtime libraries from builder
COPY --from=builder /root/.local /root/.local

# Ensure the local packages are in PATH
ENV PATH=/root/.local/bin:$PATH

# Copy the rest of the application code
COPY . /app/

# Set file permissions to the non-root user
RUN chown -R django_user:django_user /app

# Switch to non-root user
USER django_user

# Expose the Django port
EXPOSE 8000

# Command to run migrations, collect static files, and start Gunicorn
CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn project_name.wsgi:application --bind 0.0.0.0:8000 --workers=3"]

# Healthcheck to ensure the service is up
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl --fail http://localhost:8000/health/ || exit 1
