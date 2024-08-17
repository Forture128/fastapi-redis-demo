# docker/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install Poetry and setuptools (which includes distutils)
RUN pip install --upgrade pip setuptools poetry

# Copy pyproject.toml and poetry.lock if exists
COPY pyproject.toml poetry.lock* /app/

# Install dependencies via Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY ./app /app

# Command to run the FastAPI server
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]