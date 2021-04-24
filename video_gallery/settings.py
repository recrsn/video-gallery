import os

from flask import Flask


def database_uri():
    return os.getenv('DATABASE_URI')


def init_app(app: Flask):
    app.secret_key = os.getenvb(b"SECRET_KEY") or os.urandom(24)

    app.config.update(
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI=database_uri(),
        BASE_URL=os.getenv('BASE_URL', 'http://127.0.0.1:5000'),
    )
