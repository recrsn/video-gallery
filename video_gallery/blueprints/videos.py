from flask import jsonify
from flask.blueprints import Blueprint

from video_gallery.models import Video

blueprint = Blueprint('videos', __name__)


@blueprint.route('/', methods=['GET'])
def list_videos():
    response = [{
        'id': video.id,
        'title': video.title,
        'description': video.description,
        'thumbnail_url': video.thumbnail_url,
        'published_at': video.published_at,
        'indexed_at': video.indexed_at
    } for video in Video.query.all()]

    return jsonify(response)
