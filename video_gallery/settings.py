import os

from flask import Flask


def database_uri():
    return os.getenv('DATABASE_URI')


def celery_broker_uri():
    return os.getenv('CELERY_BROKER_URI')


def init_app(app: Flask):
    app.secret_key = os.getenvb(b"SECRET_KEY") or os.urandom(24)

    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI=database_uri(),
        BASE_URL=os.getenv('BASE_URL', 'http://127.0.0.1:5000'),
    )


def video_update_interval_seconds():
    return int(os.getenv('VIDEO_UPDATE_INTERVAL_SECONDS', '60'))


def youtube_search_query():
    return os.getenv('YOUTUBE_SEARCH_QUERY', 'cats')


def youtube_api_key():
    return os.getenv('YOUTUBE_API_KEY')
