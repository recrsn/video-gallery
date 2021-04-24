from datetime import datetime, timezone

from dateutil.parser import isoparse

from video_gallery.clients.youtube import YouTubeClient

API_KEY = '542d8aea-293d-42d0-96f0-3344ed39f8c9'


def test_youtube_client_returns_videos_without_published_date(mocker):
    mock_get = mocker.patch('video_gallery.clients.youtube.requests.get')
    mock_get.return_value.json.return_value = {
        'items': [
            {
                'id': {
                    'videoId': 'edd69c2d-d94a-4ae4-8bf6-e62825df768c'
                },
                'snippet': {
                    'title': 'Hello World',
                    'description': 'Description',
                    'thumbnails': {
                        'default': {
                            'url': 'https://example.com/thumbnail.jpg',
                        }
                    },
                    'publishedAt': '2021-04-24T20:53:26+05:30'
                }
            },
            {
                'id': {
                    'videoId': '8ea4af72-ca10-40d1-b07c-7a4f192c19f5'
                },
                'snippet': {
                    'title': 'Foo Bar',
                    'description': 'Spam and Eggs',
                    'thumbnails': {
                        'default': {
                            'url': 'https://example.com/spam-and-eggs.jpg',
                        }
                    },
                    'publishedAt': '2021-04-24T20:53:26+05:30'
                }
            }
        ]
    }
    client = YouTubeClient(API_KEY)

    videos = client.search('cats')

    assert videos == [
        {
            'id': 'edd69c2d-d94a-4ae4-8bf6-e62825df768c',
            'title': 'Hello World',
            'description': 'Description',
            'thumbnail_url': 'https://example.com/thumbnail.jpg',
            'published_at': isoparse('2021-04-24T20:53:26+05:30'),
        },
        {
            'id': '8ea4af72-ca10-40d1-b07c-7a4f192c19f5',
            'title': 'Foo Bar',
            'description': 'Spam and Eggs',
            'thumbnail_url': 'https://example.com/spam-and-eggs.jpg',
            'published_at': isoparse('2021-04-24T20:53:26+05:30')

        }]
    mock_get.assert_called_with('https://www.googleapis.com/youtube/v3/search', params={
        'key': API_KEY,
        'type': 'video',
        'part': 'id,snippet',
        'order': 'date',
        'maxResults': 100,
        'q': 'cats'})


def test_youtube_client_returns_videos_since_published_date(mocker):
    mock_get = mocker.patch('video_gallery.clients.youtube.requests.get')
    mock_get.return_value.json.return_value = {
        'items': [
            {
                'id': {
                    'videoId': '8ea4af72-ca10-40d1-b07c-7a4f192c19f5'
                },
                'snippet': {
                    'title': 'Foo Bar',
                    'description': 'Spam and Eggs',
                    'thumbnails': {
                        'default': {
                            'url': 'https://example.com/spam-and-eggs.jpg',
                        }
                    },
                    'publishedAt': '2021-04-24T20:53:26+05:30'
                }
            }
        ]
    }
    client = YouTubeClient(API_KEY)

    timestamp = datetime.now(tz=timezone.utc)
    videos = client.search('cats', timestamp)

    assert videos == [
        {
            'id': '8ea4af72-ca10-40d1-b07c-7a4f192c19f5',
            'title': 'Foo Bar',
            'description': 'Spam and Eggs',
            'thumbnail_url': 'https://example.com/spam-and-eggs.jpg',
            'published_at': isoparse('2021-04-24T20:53:26+05:30')

        }]
    mock_get.assert_called_with('https://www.googleapis.com/youtube/v3/search', params={
        'key': API_KEY,
        'type': 'video',
        'part': 'id,snippet',
        'order': 'date',
        'maxResults': 100,
        'q': 'cats',
        'publishedAfter': timestamp.isoformat()
    })
