# Use uv Python Alpine as the base image
FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Install dependencies
RUN apk add --no-cache caddy

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml uv.lock* ./

# Install project dependencies with uv
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of your application's code
COPY . .

# Copy Caddy configuration
COPY Caddyfile /etc/caddy/Caddyfile

# Make port 80 available to the world outside this container
EXPOSE 8000

# Set environment variables
ENV FLASK_APP=main
ENV FLASK_RUN_HOST=0.0.0.0

ENV PATH="/app/.venv/bin:$PATH"

# Create a non-root user to run the app
# RUN adduser -D appuser
# USER appuser

ENTRYPOINT []

# Run both Caddy and WaitressS
#CMD [
#"caddy", "run", "--config", "/etc/caddy/Caddyfile", "&",
#"gunicorn", "-w", "4", "main:create_app()", "--access-logfile=/var/log/gunicorn-access.log", "--error-logfile=/var/log/gunicorn-error.log"]
CMD gunicorn -w 4 'main:create_app()' --access-logfile=/var/log/gunicorn-access.log --error-logfile=/var/log/gunicorn-error.log
# CMD caddy run --config /etc/caddy/Caddyfile & gunicorn -w 4 'main:create_app()' --access-logfile=/var/log/gunicorn-access.log --error-logfile=/var/log/gunicorn-error.log
