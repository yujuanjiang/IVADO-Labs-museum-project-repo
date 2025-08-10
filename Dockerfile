FROM python:3.10-slim

# Install system dependencies for lxml, pandas, and Jupyter
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file first for layer caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install Jupyter
RUN pip install notebook jupyterlab

# Copy project files
COPY . /app/

# Expose Jupyter port
EXPOSE 8888

# Run Jupyter on container start
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

