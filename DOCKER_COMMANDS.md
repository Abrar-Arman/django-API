# Docker + uv + Django Commands Cheat Sheet

## Build and start containers

# Build fresh images
docker compose build --no-cache

# Start containers in foreground 
docker compose up

# Start containers in background (detached)
docker compose up -d

# Stop containers
docker compose down

# Stop containers and remove orphan containers
docker compose down --remove-orphans


## Database

# Run Django migrations
docker compose run web uv run python src/manage.py migrate


