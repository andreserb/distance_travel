# Use the official Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install RabbitMQ dependencies and RabbitMQ server
RUN apt-get update && \
    apt-get install -y rabbitmq-server && \
    rm -rf /var/lib/apt/lists/*

# Copy the RabbitMQ configuration file
COPY rabbitmq.config /etc/rabbitmq/

# Configure RabbitMQ to allow remote login
RUN sed -i 's/# allow_remote_login/allow_remote_login/' /etc/rabbitmq/rabbitmq.config

# Copy the requirements.txt file to the container
COPY calculate_distance/requirements.txt .

# Upgrade Python pip
RUN pip install --upgrade pip

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY calculate_distance .

# Expose the port that the application will run on
EXPOSE 8000 5672 15672

# Enable the RabbitMQ management plugin for the web interface
RUN rabbitmq-plugins enable rabbitmq_management

# Define environment variables for RabbitMQ default user and password
ENV RABBITMQ_DEFAULT_USER=guest
ENV RABBITMQ_DEFAULT_PASS=guest

# Start RabbitMQ service and the FastAPI application
CMD service rabbitmq-server start && uvicorn main:app --host 0.0.0.0 --port 8000
