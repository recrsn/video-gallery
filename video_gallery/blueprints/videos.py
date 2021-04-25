from dateutil.parser import isoparse
from flask import request, jsonify
from flask.blueprints import Blueprint
from sqlalchemy import desc

from .responses import validation_error, not_found
from ..models import Video
from ..serializers import video_serializer

DEFAULT_PAGE_SIZE = '20'

blueprint = Blueprint('videos', __name__)


@blueprint.route('', methods=['GET'])
def list_videos():
    try:
        before_query_param = request.args.get('before')
        before = isoparse(before_query_param) if before_query_param else None
    except ValueError:
        return validation_error('"before" is not a valid date')

    try:
        limit = int(request.args.get('limit', DEFAULT_PAGE_SIZE))
    except ValueError:
        return validation_error('"limit" must be a valid integer')

    if limit < 1:
        return validation_error('"limit" must be > 1')

    query = Video.query

    if before:
        query = query.filter(Video.published_at <= before)

    return jsonify(video_serializer.serialize_many(
        query.order_by(desc(Video.published_at)).limit(limit).all()))


@blueprint.route('/<video_id>', methods=['GET'])
def get_video(video_id):
    video = Video.query.filter_by(id=video_id).first()

    if not video:
        return not_found()

    return jsonify(video_serializer.serialize(video))
