from datetime import timezone


def serialize(video):
    return {
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'thumbnail_url': video.thumbnail_url,
        'published_at': video.published_at.replace(tzinfo=timezone.utc).isoformat(),
    }


def serialize_many(videos):
    return [serialize(video) for video in videos]
