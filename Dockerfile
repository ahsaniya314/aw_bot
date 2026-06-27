# Gunakan Python 3.10 slim as base
FROM python:3.10-slim

# Set non-interactive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 7860

# Install minimal system dependencies & Node.js (untuk build Next.js)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies and project
RUN pip install --no-cache-dir .

# Build Next.js Dashboard
RUN cd dashboard-web && npm install && npm run build

# Create logs directory if not exists
RUN mkdir -p logs

# Expose port for Hugging Face / Render
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
