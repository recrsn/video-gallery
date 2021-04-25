def serialize(video):
    return {
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'thumbnailUrl': video.thumbnail_url,
        # UTC dates with Zulu
        'publishedAt': video.published_at.isoformat().replace('+00:00', 'Z'),
    }


def serialize_many(videos):
    return [serialize(video) for video in videos]
