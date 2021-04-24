from flask import Flask

from . import db
from . import settings
from .blueprints import index, videos


def create_app():
    app = Flask(__name__)
    settings.init_app(app)
    db.init_app(app)

    app.register_blueprint(index.blueprint)
    app.register_blueprint(videos.blueprint, url_prefix="/v1/videos")

    return app
