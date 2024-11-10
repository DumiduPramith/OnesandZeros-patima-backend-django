# Use an official Python runtime as a parent image
FROM python:3.10

ARG BUILD_ENV

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.prod.txt /app/
COPY requirements.dev.txt /app/

RUN if [ "$BUILD_ENV" = "development" ]; then \
      pip install --no-cache-dir -r requirements.dev.txt; \
    else \
      pip install --no-cache-dir -r requirements.prod.txt; \
    fi


# Copy project
COPY . /app/