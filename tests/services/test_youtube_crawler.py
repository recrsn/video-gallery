from datetime import datetime, timezone, timedelta
from uuid import uuid4

from video_gallery import db
from video_gallery.models import Video
from video_gallery.services import youtube_crawler


def test_collect_videos_should_call_search_with_none_if_no_videos_exist(app, mocker):
    mock_latest = mocker.patch('video_gallery.services.youtube_crawler.Video.latest')
    mock_search = mocker.patch.object(youtube_crawler.client, 'search')
    mocker.patch.object(youtube_crawler.settings, 'youtube_search_query').return_value = 'cats'

    mock_latest.return_value = None
    mock_search.return_value = []

    with app.app_context():
        youtube_crawler.collect_videos()

    mock_search.assert_called_with('cats', None)


def test_collect_videos_should_call_search_with_latest_timestamp(app, mocker):
    mock_latest = mocker.patch('video_gallery.services.youtube_crawler.Video.latest')
    mock_search = mocker.patch.object(youtube_crawler.client, 'search')

    published_at = datetime.now()
    mock_latest.return_value = Video(published_at=published_at)
    mock_search.return_value = []

    with app.app_context():
        youtube_crawler.collect_videos()

    mock_search.assert_called_with('cats', published_at)


def test_collect_videos_should_store_collected_videos(app, mocker):
    mock_search = mocker.patch.object(youtube_crawler.client, 'search')

    with app.app_context():
        Video.query.delete()

        published_at = datetime.now(tz=timezone.utc)

        with db.transaction():
            db.persist(Video(id='yt-' + str(uuid4()),
                             title='Hello World',
                             description='Hello World',
                             thumbnail_url='https://example.com/65c14152.jpg',
                             published_at=published_at))

        mock_search.return_value = [
            {
                'id': 'abcd',
                'title': 'Hello World',
                'description': 'Hello World',
                'thumbnail_url': 'https://example.com/image.jpg',
                'published_at': published_at + timedelta(seconds=300)
            }
        ]

        youtube_crawler.collect_videos()

        mock_search.assert_called_with('cats', published_at)

        assert Video.latest().id == 'yt-abcd'
