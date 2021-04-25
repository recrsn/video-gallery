from flask import jsonify


def validation_error(messages):
    return jsonify({
        'message': 'Validation error',
        'errors': messages
    }), 400


def error_body(message):
    return jsonify({'message': message})


def not_found(message="Not found"):
    return error_body(message), 404
