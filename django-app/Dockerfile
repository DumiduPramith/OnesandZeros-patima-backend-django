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

RUN python -m pip install --upgrade pip

RUN if [ "$BUILD_ENV" = "development" ]; then \
      pip install --no-cache-dir -r requirements.dev.txt; \
    else \
      pip install --no-cache-dir -r requirements.prod.txt; \
    fi

# Download Tensoflow-wheel and install
RUN if [ "$BUILD_ENV" = "production" ]; then \
    wget https://storage.googleapis.com/tensorflow/versions/2.18.0/tensorflow-2.18.0-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl; \
    pip install tensorflow-2.18.0-cp310-cp310-manylinux_2_17_aarch64.manylinux2014_aarch64.whl; \
    fi

# Install Tensorflow

# Copy project
COPY . /app/