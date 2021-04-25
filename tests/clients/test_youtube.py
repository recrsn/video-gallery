from datetime import datetime, timezone
from unittest.mock import MagicMock, call

import pytest
import requests
from dateutil.parser import isoparse
from requests import HTTPError

from video_gallery.clients.youtube import YouTubeClient

API_KEY = ['542d8aea-293d-42d0-96f0-3344ed39f8c9', 'cb0b8a90-3e73-43be-8f07-8778f15b1b97']


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
        'key': API_KEY[0],
        'type': 'video',
        'part': 'id,snippet',
        'order': 'date',
        'maxResults': 1000,
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
        'key': API_KEY[0],
        'type': 'video',
        'part': 'id,snippet',
        'order': 'date',
        'maxResults': 1000,
        'q': 'cats',
        'publishedAfter': timestamp.isoformat()
    })


def good_response(json):
    response = MagicMock()
    response.ok = True
    response.status_code = 200
    response.json.return_value = json

    return response


def test_youtube_client_uses_different_api_key_if_one_is_unavailable(mocker):
    def mock_requests_get(_, params):
        if params['key'] == '542d8aea-293d-42d0-96f0-3344ed39f8c9':
            bad_response = MagicMock()
            bad_response.ok = False
            bad_response.status_code = 403
            bad_response.json.return_value = {
                "error": {
                    "errors": [
                        {
                            "domain": "youtube.quota",
                            "reason": "quotaExceeded"
                        }
                    ]
                }
            }

            return bad_response

        return good_response({
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
        })

    mock_get = mocker.patch('video_gallery.clients.youtube.requests.get')
    mock_get.side_effect = mock_requests_get

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
    mock_get.assert_any_call('https://www.googleapis.com/youtube/v3/search', params={
        'key': API_KEY[0],
        'type': 'video',
        'part': 'id,snippet',
        'order': 'date',
        'maxResults': 1000,
        'q': 'cats',
        'publishedAfter': timestamp.isoformat()
    })
    mock_get.assert_called_with('https://www.googleapis.com/youtube/v3/search', params={
        'key': API_KEY[1],
        'type': 'video',
        'part': 'id,snippet',
        'order': 'date',
        'maxResults': 1000,
        'q': 'cats',
        'publishedAfter': timestamp.isoformat()
    })


def test_youtube_client_raises_exception_if_no_api_key_is_available(mocker):
    bad_response = MagicMock()
    bad_response.ok = False
    bad_response.status_code = 403
    bad_response.json.return_value = {
        "error": {
            "errors": [
                {
                    "domain": "youtube.quota",
                    "reason": "quotaExceeded"
                }
            ]
        }
    }

    mock_get = mocker.patch('video_gallery.clients.youtube.requests.get')
    mock_get.return_value = bad_response

    client = YouTubeClient(API_KEY)

    timestamp = datetime.now(tz=timezone.utc)

    with pytest.raises(RuntimeError) as exc_info:
        client.search('cats', timestamp)

    assert str(exc_info.value) == 'No API keys available'

    with pytest.raises(RuntimeError) as exc_info:
        client.search('cats', timestamp)

    assert str(exc_info.value) == 'No API keys available'

    mock_get.assert_has_calls((
        call('https://www.googleapis.com/youtube/v3/search', params={
            'key': API_KEY[0],
            'type': 'video',
            'part': 'id,snippet',
            'order': 'date',
            'maxResults': 1000,
            'q': 'cats',
            'publishedAfter': timestamp.isoformat()
        }),
        call().json(),
        call('https://www.googleapis.com/youtube/v3/search', params={
            'key': API_KEY[1],
            'type': 'video',
            'part': 'id,snippet',
            'order': 'date',
            'maxResults': 1000,
            'q': 'cats',
            'publishedAfter': timestamp.isoformat()
        })),
        call().json())


def test_youtube_client_raises_exception_for_403_if_not_quota_exceeded(mocker):
    def http_error():
        raise HTTPError('Forbidden')

    bad_response = MagicMock(requests.Response)
    bad_response.ok = False
    bad_response.status_code = 403
    bad_response.raise_for_status.side_effect = http_error
    bad_response.json.return_value = {
        "error": {
            "code": 403,
            "errors": [
                {
                    "domain": "global",
                    "reason": "forbidden"
                }
            ]
        }
    }

    mock_get = mocker.patch('video_gallery.clients.youtube.requests.get')
    mock_get.return_value = bad_response

    client = YouTubeClient(API_KEY)

    timestamp = datetime.now(tz=timezone.utc)

    with pytest.raises(HTTPError) as exc_info:
        client.search('cats', timestamp)

    assert str(exc_info.value) == 'Forbidden'

    mock_get.assert_called_once_with('https://www.googleapis.com/youtube/v3/search', params={
        'key': API_KEY[0],
        'type': 'video',
        'part': 'id,snippet',
        'order': 'date',
        'maxResults': 1000,
        'q': 'cats',
        'publishedAfter': timestamp.isoformat()
    })


def test_youtube_client_raises_exception_for_http_error(mocker):
    def http_error():
        raise HTTPError('Internal server error')

    bad_response = MagicMock(requests.Response)
    bad_response.ok = False
    bad_response.status_code = 500
    bad_response.raise_for_status.side_effect = http_error

    mock_get = mocker.patch('video_gallery.clients.youtube.requests.get')
    mock_get.return_value = bad_response

    client = YouTubeClient(API_KEY)

    timestamp = datetime.now(tz=timezone.utc)

    with pytest.raises(HTTPError) as exc_info:
        client.search('cats', timestamp)

    assert str(exc_info.value) == 'Internal server error'

    mock_get.assert_called_once_with('https://www.googleapis.com/youtube/v3/search', params={
        'key': API_KEY[0],
        'type': 'video',
        'part': 'id,snippet',
        'order': 'date',
        'maxResults': 1000,
        'q': 'cats',
        'publishedAfter': timestamp.isoformat()
    })
