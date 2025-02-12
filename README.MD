# Courses Catalog Application

A simple courses catalog application with HTML frontend and FastAPI backend.

## Project Structure

- `frontend/`: HTML frontend
- `backend/`: FastAPI backend
- `requirements.txt`: Python dependencies
- `Dockerfile`: Docker configuration
- `docker-compose.yml`: Docker Compose configuration

## Setup

1. Clone the repository

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the application

```bash
python main.py
```

## Docker

### Using Docker Directly

1. Build and run

```bash

docker build -t courses-catalog .
docker run -d -p 8000:8000 courses-catalog
```

2. Stop and cleanup

```bash
docker stop courses-catalog
docker rm courses-catalog
```

### Using Docker Compose

1. Start the application

```bash
docker-compose up -d
```

2. View container logs

```bash
docker-compose logs -f
```

3. Access container shell

```bash
docker-compose exec app bash
```

4. Stop and cleanup

```bash
# Stop and remove containers
docker-compose down

# Stop, remove containers and delete images
docker-compose down --rmi all
```
