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
## Getting Started

### Prerequisites

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

## Key Features

- **FastAPI Integration**: A high-performance web framework for building APIs.
- **Redis as a Cache**: Utilize Redis as an in-memory key-value store for caching API responses.
- **PostgreSQL Integration**: Leverage PostgreSQL, a powerful open-source relational database, with full async support.
- **Asynchronous Operations**: Full support for async operations using asyncpg and SQLAlchemy.
- **Alembic Migrations**: Manage and apply database schema changes with Alembic.
- **Docker Integration**: Easily manage and run Redis and PostgreSQL using Docker and Docker Compose.


## Usage
### API Endpoints

1. **Create User**
    - **Endpoint:** `POST /users/`
    - **Example Request:**
        
        ```json
        {
          "name": "John Doe",
          "email": "john.doe@example.com"
        }
        
        ```
        
    - **Example Response:**
        
        ```json
        {
          "id": 1,
          "name": "John Doe",
          "email": "john.doe@example.com"
        }
        
        ```
        
2. **Get User By ID**
    - **Endpoint:** `GET /users/{user_id}`
    - **Example Request:** `GET /users/1`
    - **Example Response:**
        
        ```json
        {
          "id": 1,
          "name": "John Doe",
          "email": "john.doe@example.com"
        }
        
        ```
        
3. **Redis Cache Example**
    - **Endpoint:** `GET /cache/`
    - **Example Response:**
        
        ```json
        {
          "cached_value": "Hello, Redis!"
        }
        
        ```
        
4. **Leaderboard Example**
    - **Add a Score to the Leaderboard:**
        - **Endpoint:** `POST /leaderboard/`
        - **Example Request:**
            
            ```json
            {
              "user_id": "user1",
              "score": 1500
            }
            
            ```
            
        - **Example Response:**
            
            ```json
            {
              "message": "Score added"
            }
            
            ```
            
    - **Retrieve the Leaderboard:**
        - **Endpoint:** `GET /leaderboard/`
        - **Example Request:** `GET /leaderboard/?top_n=5`
        - **Example Response:**
            
            ```json
            {
              "leaderboard": [
                ["user1", 1500],
                ["user2", 1200],
                ["user3", 900]
              ]
            }
            
            ```
            
5. **Proximity Search Example**
    - **Add a Location:**
        - **Endpoint:** `POST /locations/`
        - **Example Request:**
            
            ```json
            {
              "name": "Central Park",
              "longitude": -73.965355,
              "latitude": 40.782865
            }
            
            ```
            
        - **Example Response:**
            
            ```json
            {
              "message": "Location 'Central Park' added."
            }
            
            ```
            
    - **Find Nearby Locations:**
        - **Endpoint:** `GET /locations/`
        - **Example Request:** `GET /locations/?longitude=-73.965355&latitude=40.782865&radius=5&unit=km`
        - **Example Response:**
            
            ```json
            {
              "nearby_locations": [
                ["Central Park", 0.0, [-73.965355, 40.782865]]
              ]
            }
            
            ```
            
6. **Event Sourcing Example with Redis Streams**
    - **Add an Event to a Stream:**
        - **Endpoint:** `POST /streams/orders/events/`
        - **Example Request:**
            
            ```json
            {
              "event_data": {
                "order_id": "123",
                "status": "created"
              }
            }
            
            ```
            
        - **Example Response:**
            
            ```json
            {
              "event_id": "1637855101770-0"
            }
            
            ```
            
    - **Create a Consumer Group:**
        - **Endpoint:** `POST /streams/orders/groups/order-group/`
        - **Example Request:**
            
            ```json
            {
              "group_name": "order-group"
            }
            
            ```
            
        - **Example Response:**
            
            ```json
            {
              "message": "Consumer group 'order-group' created for stream 'orders'."
            }
            
            ```
            
    - **Read Events from the Stream:**
        - **Endpoint:** `GET /streams/orders/groups/order-group/events/`
        - **Example Request:** `GET /streams/orders/groups/order-group/events/?consumer_name=consumer-1&count=5`
        - **Example Response:**
            
            ```json
            {
              "events": [
                [
                  "orders",
                  [
                    [
                      "1637855101770-0",
                      {
                        "order_id": "123",
                        "status": "created"
                      }
                    ]
                  ]
                ]
              ]
            }
            
            ```
            
    - **Acknowledge Processed Events:**
        - **Endpoint:** `POST /streams/orders/groups/order-group/acknowledge/`
        - **Example Request:**
            
            ```json
            {
              "event_id": "1637855101770-0"
            }
            
            ```
            
        - **Example Response:**
            
            ```json
            {
              "message": "Event '1637855101770-0' acknowledged."
            }
            
            ```
            

## Advanced Redis Use Cases

### Distributed Locks

- **Description**: Ensures that multiple instances of a service do not perform the same operation simultaneously.
- **Implementation**: Uses Redis to implement distributed locks with expiration times to handle critical sections in a distributed environment.

### Leaderboards

- **Description**: Efficiently manage and query leaderboards using Redis Sorted Sets.
- **Implementation**: Store user scores in a sorted set and retrieve the top N users.

### Proximity Search

- **Description**: Use Redis geospatial features to perform proximity searches.
- **Implementation**: Add locations to a Redis geospatial index and perform radius searches to find nearby points.

### Event Sourcing

- **Description**: Store and replay sequences of events to rebuild system state.
- **Implementation**: Use Redis Streams for append-only logs and manage consumer groups for processing events.


## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or suggestions.