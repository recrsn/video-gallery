from datetime import timezone, datetime
from uuid import uuid4

from video_gallery import db
from video_gallery.models import Video
from video_gallery.serializers import video_serializer


def test_list_videos_throws_error_for_invalid_date(client):
    response = client.get('/v1/videos?before=abcd')

    assert response.status == '400 BAD REQUEST'
    assert response.content_type == 'application/json'
    assert response.json == {'errors': '"before" is not a valid date',
                             'message': 'Validation error'}


def test_list_videos_throws_error_for_invalid_limit(client):
    response = client.get('/v1/videos?limit=abcd')

    assert response.status == '400 BAD REQUEST'
    assert response.content_type == 'application/json'
    assert response.json == {'errors': '"limit" must be a valid integer',
                             'message': 'Validation error'}


def test_list_videos_throws_error_for_illegal_limit(client):
    response = client.get('/v1/videos?limit=-22')

    assert response.status == '400 BAD REQUEST'
    assert response.content_type == 'application/json'
    assert response.json == {'errors': '"limit" must be > 1', 'message': 'Validation error'}


def test_list_videos_returns_videos_with_default_limit_and_offset(app, client):
    with app.app_context():
        with db.transaction():
            Video.query.delete()
            videos = [Video(
                id=str(uuid4()),
                title=f'Video {i}',
                description='description',
                thumbnail_url="https://example.com/74ced8c7.jpg",
                published_at=datetime(year=2021, month=4, day=24, hour=23, minute=15, second=i,
                                      tzinfo=timezone.utc)
            ) for i in range(25)]
            db.persist_all(videos)

        response = client.get('/v1/videos')

        assert response.status == '200 OK'
        assert response.content_type == 'application/json'
        assert response.json == video_serializer.serialize_many(list(reversed(videos[-20:])))


def test_list_videos_returns_videos_with_time_offset(app, client):
    with app.app_context():
        with db.transaction():
            Video.query.delete()
            videos = [Video(
                id=str(uuid4()),
                title=f'Video {i}',
                description='description',
                thumbnail_url="https://example.com/74ced8c7.jpg",
                published_at=datetime(year=2021, month=4, day=24, hour=23, minute=15, second=i,
                                      tzinfo=timezone.utc)
            ) for i in range(25)]
            db.persist_all(videos)

        response = client.get('/v1/videos?before=2021-04-24T23:15:05Z')

        assert response.status == '200 OK'
        assert response.content_type == 'application/json'
        assert response.json == video_serializer.serialize_many(list(reversed(videos[:6])))


def test_list_videos_returns_videos_with_limit(app, client):
    with app.app_context():
        with db.transaction():
            Video.query.delete()
            videos = [Video(
                id=str(uuid4()),
                title=f'Video {i}',
                description='description',
                thumbnail_url="https://example.com/74ced8c7.jpg",
                published_at=datetime(year=2021, month=4, day=24, hour=23, minute=15, second=i,
                                      tzinfo=timezone.utc)
            ) for i in range(25)]
            db.persist_all(videos)

        response = client.get('/v1/videos?limit=5')

        assert response.status == '200 OK'
        assert response.content_type == 'application/json'
        assert response.json == video_serializer.serialize_many(list(reversed(videos[-5:])))
