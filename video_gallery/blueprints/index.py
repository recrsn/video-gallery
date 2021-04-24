from flask import jsonify
from flask.blueprints import Blueprint

blueprint = Blueprint('index', __name__)


@blueprint.route('/')
def index():
    return jsonify({
        'message': 'OK'
    })
