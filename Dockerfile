FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /code

# Copy project files into the Docker image
COPY . /code/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn -b :$PORT core.wsgi