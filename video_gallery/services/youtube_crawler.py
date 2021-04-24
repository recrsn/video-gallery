from sqlalchemy.dialects.postgresql import insert

from .. import settings, db
from ..clients.youtube import YouTubeClient
from ..models import Video

client = YouTubeClient(settings.youtube_api_key())


def get_id_for_provider(_id):
    return f'yt-{_id}'


def collect_videos():
    last_video = Video.latest()

    published_after = last_video.published_at if last_video else None

    # TODO: optimize with ETags and If-Modified-Since when published_after is same
    videos = client.search(settings.youtube_search_query(), published_after)

    for video in videos:
        video['id'] = get_id_for_provider(video['id'])

    if len(videos):
        with db.transaction():
            stmt = insert(Video).values(videos).on_conflict_do_nothing()
            db.execute(stmt)
