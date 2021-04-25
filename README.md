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

## API

### To get a list of videos with pagination

Params:
- `limit` -- [Integer] Count of videos to return
- `before` -- [Date] Ex: 2021-04-25T07:42:56Z

```http request
GET localhost:5000/v1/videos?limit=2&since=2021-04-25T07:42:56Z

Connection: close
Content-Length: 1146
Content-Type: application/json
Date: Sun, 25 Apr 2021 11:41:37 GMT
Server: gunicorn

[
    {
        "description": "More cats on catkotes2 channel.",
        "id": "yt-7yryWp2b-HI",
        "publishedAt": "2021-04-25T11:37:55Z",
        "thumbnailUrl": "https://i.ytimg.com/vi/7yryWp2b-HI/default.jpg",
        "title": "funny cat 10 sec"
    },
    {
        "description": "More cats on catkotes2 channel.",
        "id": "yt-YC1ETK2ouQs",
        "publishedAt": "2021-04-25T11:36:55Z",
        "thumbnailUrl": "https://i.ytimg.com/vi/YC1ETK2ouQs/default.jpg",
        "title": "what cats hate"
    }
]
```

### To get a list of videos with a search query

Params:
- `limit` -- [Integer] Count of videos to return
- `before` -- [Date] Date filter Ex: 2021-04-25T07:42:56Z
- `q` -- [String] Search string

```http request
GET localhost:5000/v1/videos?limit=2&since=2021-04-25T07:42:56Z

Connection: close
Content-Length: 1146
Content-Type: application/json
Date: Sun, 25 Apr 2021 11:41:37 GMT
Server: gunicorn

[
    {
        "description": "More cats on catkotes2 channel.",
        "id": "yt-7yryWp2b-HI",
        "publishedAt": "2021-04-25T11:37:55Z",
        "thumbnailUrl": "https://i.ytimg.com/vi/7yryWp2b-HI/default.jpg",
        "title": "funny cat 10 sec"
    },
    {
        "description": "More cats on catkotes2 channel.",
        "id": "yt-YC1ETK2ouQs",
        "publishedAt": "2021-04-25T11:36:55Z",
        "thumbnailUrl": "https://i.ytimg.com/vi/YC1ETK2ouQs/default.jpg",
        "title": "what cats hate"
    }
]
