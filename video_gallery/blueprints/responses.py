from flask import jsonify


def validation_error(messages):
    return jsonify({
        'message': 'Validation error',
        'errors': messages
    }), 400
