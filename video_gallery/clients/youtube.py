import requests
from dateutil.parser import isoparse

YOUTUBE_API_ENDPOINT = 'https://www.googleapis.com/youtube'


def get_youtube_video(item):
    snippet = item['snippet']
    return {
        'id': item['id']['videoId'],
        'title': snippet['title'],
        'description': snippet['description'],
        'thumbnail_url': snippet['thumbnails']['default']['url'],
        'published_at': isoparse(snippet['publishedAt'])
    }


def quota_expired(response):
    if response.status_code != 403:
        return False

    return response.json().get('error', {}).get('errors')[0]["reason"] == 'quotaExceeded'


class YouTubeClient:

    def __init__(self, api_keys):
        # TODO: handle key reuse
        self.__api_keys = [{'key': key, 'available': True} for key in api_keys]

    def __http_get(self, endpoint, params):
        for item in self.__api_keys:
            if item['available']:
                response = requests.get(YOUTUBE_API_ENDPOINT + endpoint,
                                        params={**params, **{'key': item['key']}})

                if response.ok:
                    return response.json()

                if quota_expired(response):
                    item['available'] = False
                else:
                    response.raise_for_status()

        raise RuntimeError('No API keys available')

    def search(self, query, published_after=None):
        search_params = {
            'type': 'video',
            'part': 'id,snippet',
            'order': 'date',
            'maxResults': 1000,
            'q': query,
        }

        if published_after:
            search_params['publishedAfter'] = published_after.isoformat()

        response = self.__http_get('/v3/search', params=search_params)

        return [get_youtube_video(item) for item in response["items"]]
