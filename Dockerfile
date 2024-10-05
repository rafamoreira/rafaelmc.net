# Use Python Alpine as the base image
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock* ./

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of your application's code
COPY . .

# Install Caddy
RUN apk add --no-cache caddy

# Copy Caddy configuration
COPY Caddyfile /etc/caddy/Caddyfile

# Make port 80 available to the world outside this container
EXPOSE 80

# Set environment variables
ENV FLASK_APP=main
ENV FLASK_RUN_HOST=0.0.0.0

# Create a non-root user to run the app
# RUN adduser -D appuser
# USER appuser

# Run both Caddy and Waitress
CMD caddy run --config /etc/caddy/Caddyfile & waitress-serve --call main:create_app
