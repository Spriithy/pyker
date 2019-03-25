from flask import *
import json
import state
import random

bp = Blueprint('conn', __name__, url_prefix='/v0/conn')

users = {}


def username(session):
    return '%s#%s' % (session['user.name'], session['user.id'])


@bp.route('/get/users')
def get_users():
    return Response(
        '{"state": "OK", "message": "", "payload.type": "user.list", "user.list": '
        + json.dumps(users) + '}',
        mimetype='text/json')


@bp.route('/init', methods=['POST'])
def init():
    session['user.name'] = request.form.get('user.name', None)
    session['user.id'] = str(random.randint(2134, 8976))
    session['state'] = state.NO_LOBBY
    if not session['user.name']:
        return Response(
            '{"status": "ERROR", "message": "username not set"}',
            mimetype='text/json')
    users[username(session)] = {**session}
    return Response(
        '{"status": "OK", "message": "connection established", "user.name": "%s", "user.id": "%s"}'
        % (session['user.name'], session['user.id']),
        mimetype='text/json')


@bp.route('/drop')
def drop():
    del users[username(session)]
    session.clear()
    return Response(
        '{"status": "OK", "message": "connection dropped"}',
        mimetype='text/json')
