import requests
from dateutil.parser import isoparse

YOUTUBE_API_ENDPOINT = 'https://www.googleapis.com/youtube'
SEARCH_URL = '/v3/search'


def get_youtube_video(item):
    snippet = item['snippet']
    return {
        'id': item['id']['videoId'],
        'title': snippet['title'],
        'description': snippet['description'],
        'thumbnail_url': snippet['thumbnails']['default']['url'],
        'published_at': isoparse(snippet['publishedAt'])
    }


class YouTubeClient:

    def __init__(self, api_key):
        self.__api_key = api_key

    def search(self, query, published_after=None):
        search_params = {
            'key': self.__api_key,
            'type': 'video',
            'part': 'id,snippet',
            'order': 'date',
            'maxResults': 100,
            'q': query,
        }

        if published_after:
            search_params['publishedAfter'] = published_after.isoformat()

        response = requests.get(YOUTUBE_API_ENDPOINT + SEARCH_URL, params=search_params)
        response.raise_for_status()

        return [get_youtube_video(item) for item in response.json()["items"]]
