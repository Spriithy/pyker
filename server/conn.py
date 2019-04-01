from flask import *
from helpers import username
import json
import state
import random
import datetime
import lobby

bp = Blueprint('conn', __name__, url_prefix='/v0/conn')

users = {}


@bp.route('/ping')
def ping():
    users[username(session)]['last_ping'] = datetime.datetime.now()
    return Response()


@bp.route('/get/users')
def get_users():
    timed_out_users = list(
        filter(
            lambda user: datetime.datetime.now() - user['last_ping'] >=
            datetime.timedelta(seconds=3), users.values()))
    for user in timed_out_users:
        lobby.broadcast('%s timed out' % username(user), standalone=True)
        del users[username(user)]
    return Response(
        '{"state": "OK", "message": "", "payload.type": "user.list", "user.list": '
        + json.dumps({
            username(user): {k: user[k]
                             for k in ('user.name', 'user.id')}
            for user in users.values()
        }) + '}',
        mimetype='text/json')


@bp.route('/init', methods=['POST'])
def init():
    session['user.name'] = request.form.get('user.name', None)
    session['user.id'] = str(random.randint(2134, 8976))
    session['state'] = state.NO_LOBBY
    session['last_ping'] = datetime.datetime.now()
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
    user = username(session)
    if user in users:
        del users[user]
    lobby.broadcast('%s disconnected' % username(session), standalone=True)
    session.clear()
    return Response(
        '{"status": "OK", "message": "connection dropped"}',
        mimetype='text/json')
