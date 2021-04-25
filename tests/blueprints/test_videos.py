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


def test_get_video_returns_404_for_non_existent_video(app, client):
    with app.app_context():
        with db.transaction():
            Video.query.delete()

    response = client.get('/v1/videos/8b123b17-5198-4d0b-8a69-47d16ec6f679')

    assert response.status == '404 NOT FOUND'
    assert response.content_type == 'application/json'
    assert response.json == {
        "message": "Not found"
    }


def test_list_videos_return_videos_for_given_id(app, client):
    with app.app_context():
        with db.transaction():
            Video.query.delete()
            video = Video(
                id='yt-1234-5678',
                title='Video',
                description='description',
                thumbnail_url="https://example.com/74ced8c7.jpg",
                published_at=datetime(year=2021, month=4, day=24, hour=23, minute=15, second=0,
                                      tzinfo=timezone.utc)
            )
            db.persist(video)

        response = client.get('/v1/videos/yt-1234-5678')

        assert response.status == '200 OK'
        assert response.content_type == 'application/json'
        assert response.json == {
            'id': 'yt-1234-5678',
            'title': 'Video',
            'description': 'description',
            'thumbnailUrl': 'https://example.com/74ced8c7.jpg',
            'publishedAt': '2021-04-24T23:15:00Z'
        }


def test_list_videos_return_videos_for_given_search_string_in_title_and_description(app, client):
    with app.app_context():
        with db.transaction():
            Video.query.delete()
            videos = [
                Video(
                    id='yt-1234-5678',
                    title='Video 1',
                    description='Cat playing with yarn',
                    thumbnail_url="https://example.com/74ced8c7.jpg",
                    published_at=datetime(year=2021, month=4, day=24, hour=23, minute=15, second=0,
                                          tzinfo=timezone.utc)
                ),
                Video(
                    id='yt-29b79965-4468-497a-b076-d603607afeb7',
                    title='Video of cats',
                    description='description',
                    thumbnail_url="https://example.com/74ced8c7.jpg",
                    published_at=datetime(year=2021, month=4, day=24, hour=23, minute=15, second=25,
                                          tzinfo=timezone.utc)
                ),
                Video(
                    id='yt-c92f5a74-5561-4bf1-b713-f56723d22228',
                    title='Awesome cats and dogs',
                    description='Cats and dogs',
                    thumbnail_url="https://example.com/74ced8c7.jpg",
                    published_at=datetime(year=2021, month=4, day=24, hour=23, minute=15, second=25,
                                          tzinfo=timezone.utc)
                ),
                Video(
                    id='yt-1234',
                    title='Dog Video',
                    description='description',
                    thumbnail_url="https://example.com/74ced8c7.jpg",
                    published_at=datetime(year=2021, month=4, day=24, hour=23, minute=15, second=2,
                                          tzinfo=timezone.utc)
                ),
            ]
            db.persist_all(videos)

        response = client.get('/v1/videos?q=cat')

        assert response.status == '200 OK'
        assert response.content_type == 'application/json'
        assert response.json == [
            {
                'description': 'description',
                'id': 'yt-29b79965-4468-497a-b076-d603607afeb7',
                'publishedAt': '2021-04-24T23:15:25Z',
                'thumbnailUrl': 'https://example.com/74ced8c7.jpg',
                'title': 'Video of cats'
            },
            {
                'description': 'Cats and dogs',
                'id': 'yt-c92f5a74-5561-4bf1-b713-f56723d22228',
                'publishedAt': '2021-04-24T23:15:25Z',
                'thumbnailUrl': 'https://example.com/74ced8c7.jpg',
                'title': 'Awesome cats and dogs'
            },
            {
                'description': 'Cat playing with yarn',
                'id': 'yt-1234-5678',
                'publishedAt': '2021-04-24T23:15:00Z',
                'thumbnailUrl': 'https://example.com/74ced8c7.jpg',
                'title': 'Video 1'
            }
        ]
