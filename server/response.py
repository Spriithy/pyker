import json


def ok(**kwargs):
    return json.dumps({'status': 'OK', 'message': '', **kwargs})


def error(message, **kwargs):
    return json.dumps({'status': 'ERROR', 'message': message, **kwargs})
