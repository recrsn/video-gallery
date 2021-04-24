from celery import Celery

from . import settings
from .services import youtube_crawler
from .wsgi import app as flask_app

app = Celery('tasks', broker=settings.celery_broker_uri())

app.conf.beat_schedule = {
    'update-youtube-videos': {
        'task': 'video_gallery.tasks.update_youtube_videos',
        'schedule': settings.video_update_interval_seconds()
    },
}


@app.task
def update_youtube_videos():
    with flask_app.app_context():
        youtube_crawler.collect_videos()
