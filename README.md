# fastapi-redis-demo
FastAPI with Redis: A Comprehensive Deep Dive
# FastAPI Redis Demo

## Overview

This project is a comprehensive demonstration of integrating FastAPI with Redis and PostgreSQL. It covers various use cases, including using Redis as a cache, implementing distributed locks, creating leaderboards, proximity search, and event sourcing.

The application is built using FastAPI, with Redis and PostgreSQL running in Docker containers. It also demonstrates the use of asynchronous database operations with SQLAlchemy and asyncpg.

## Project Structure

```plaintext
fastapi-redis-demo/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   └── user.py
│   ├── crud/
│   │   └── user.py
│   ├── schemas/
│   │   └── user.py
│   └── database.py
│
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│
├── docker/
│   ├── Dockerfile
├── docker-compose.yml
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
│
├── tests/
│   └── test_main.py
│
├── pyproject.toml
├── alembic.ini
└── README.md
```
### Getting Started

Prerequisites
- Python 3.11+
- Docker and Docker Compose
- Poetry (for dependency management)

### Installation
1. Clone the repository
    ```bash
    git clone https://github.com/yourusername/fastapi-redis-demo.git
    cd fastapi-redis-demo
    ```
2. Install dependencies using Poetry
    ```bash
    poetry install
    ```
3. Start Redis and PostgreSQL using Docker Compose:
    ```bash
    docker-compose up -d
    ```
4. Run database migrations:
    ```bash
    alembic upgrade head
    ```
5. Start the FastAPI server:
    ```bash
    poetry run uvicorn app.main:app --reload
    ```
The server will be available at http://localhost:8000.

### Key Features

- FastAPI Integration: A high-performance web framework for building APIs.
- Redis as a Cache: Fast in-memory key-value store for caching API responses.
- PostgreSQL Integration: A powerful, open-source relational database.
- Asynchronous Operations: Full async support with asyncpg and SQLAlchemy.
- Alembic Migrations: Manage and apply database schema changes.


## Usage

- API Endpoints

- Create User

- Get User By ID

- Redis Cache Example

- Running Tests


### Advanced Redis Use Cases (Coming Soon)

- Distributed Locks: Ensuring that multiple instances of a service don’t perform the same operation simultaneously.
- Leaderboards: Efficiently managing and querying leaderboards.
- Proximity Search: Using geospatial indexing for searching locations.
- Event Sourcing: Storing and replaying sequences of events.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or suggestions.