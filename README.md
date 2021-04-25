# Video Gallery

Video Gallery made by scraping YouTube API

## Usage

### Requirements

- python 3.9
- Pipenv
- Docker (for integration tests)

### Steps

1. Activate Pipenv environment with `pipenv shell`
2. Install dependencies with `pipenv install --dev`
1. Copy `.env.example` to `.env` and modify the required values.
2. Apply migrations to database using `flask db upgrade`
3. Run tests with `make tests`

## Running with docker

1. Copy `.env.example` to `.env` and modify the required values.
2. Run `docker compose -f docker-compose.yml -f docker-compose.deploy.yml up` to bring the project up
3. Apply migrations with `docker compose -f docker-compose.yml -f docker-compose.deploy.yml exec app flask db upgrade`
