FROM python:3.9-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Copy the application into the container.

COPY . /app

WORKDIR /app

RUN uv sync --frozen --no-cache

# Install the application dependencies.


# Run the application.
CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "5000", "--host", "0.0.0.0"]

EXPOSE 5000