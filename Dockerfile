# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Copy repository into the Docker image
COPY . /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Run setup.py to install dependencies
RUN pip install --upgrade pip && \
    python3 scripts/setup.py --no-sudo

# Default command (optional, if you want to use this image interactively)
CMD ["bash"]
