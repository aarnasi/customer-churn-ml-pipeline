FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl gnupg && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo "deb http://packages.cloud.google.com/apt cloud-sdk main" > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update && apt-get install -y google-cloud-sdk

# Install Python packages
RUN pip install --no-cache-dir kfp==2.4.0

