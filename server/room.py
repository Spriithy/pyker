from flask import *
from helpers import username
import json
import random
import lobby
import state

bp = Blueprint('room', __name__, url_prefix='/v0/room')

rooms = {}


def user_room(user):
    for room in rooms.values():
        if user in room['users']:
            return room
    return None


def drop_user_from_room(room, user):
    room['users'].remove(user)
    lobby.broadcast('%s left room %s' % (user, room['name']))
    if len(room['users']) == 0:
        del rooms[room['name']]
        lobby.broadcast(
            'Room %s has been automatically removed' % room['name'],
            standalone=True)


@bp.route('/list')
def list_rooms():
    return Response(
        '{"status": "OK", "message": "", "payload.type": "room.list", "room.list": '
        + json.dumps(list(map(lambda t: rooms[t], rooms))) + '}',
        mimetype='text/json')


@bp.route('/init', methods=['POST'])
def init():
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby"}',
            mimetype='text/json')

    user = username(session)
    room_id = str(random.randint(0, 1000))
    room_name = request.form.get('room.name', 'room#%s' % room_id)

    if rooms.get(room_name, None):
        lobby.broadcast(
            'Room %s already exists' % (room_name),
            dest=username(session),
            level="Error",
            standalone=True)
        return Response(
            '{"status": "OK", "message": "room already exists", "room.name": "%s"}'
            % (room_name),
            mimetype='text/json')

    prev_room = user_room(user)
    if prev_room:
        drop_user_from_room(prev_room, user)
        lobby.warning(
            'You have automatically been removed from room %s' %
            prev_room['name'],
            dest=user,
            standalone=True)

    rooms[room_name] = {
        "name": room_name,
        "id": room_id,
        "users": [user],
    }

    lobby.broadcast('%s created room %s' % (user, room_name))

    return Response(
        '{"status": "OK", "message": "room created", "room.name": "%s", "room.id": "%s"}'
        % (room_name, room_id),
        mimetype='text/json')


@bp.route('/get')
def get():
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby", "payload.type": "str", "str": ""}',
            mimetype='text/json')
    user = username(session)
    room = user_room(user)
    if room:
        return Response(
            '{"status": "OK", "message": "", "payload.type": "str", "str": "%s"}'
            % room['name'],
            mimetype='text/json')
    else:
        return Response(
            '{"status": "OK", "message": "user not in room", "payload.type": "str", "str": ""}',
            mimetype='text/json')


@bp.route('/join/<room_name>')
def join(room_name):
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby"}',
            mimetype='text/json')

    user = username(session)
    prev_room = user_room(user)
    if prev_room:
        drop_user_from_room(prev_room, user)
        lobby.warning(
            'You have automatically been removed from room %s' %
            prev_room['name'],
            dest=user,
            standalone=True)

    if not rooms.get(room_name, None):
        lobby.error(
            'room %s does not exist' % room_name, dest=user, standalone=True)
        return Response(
            '{"status": "ERROR", "message": "no such room %s"}' % room_name,
            mimetype='text/json')

    rooms[room_name]['users'].append(user)
    lobby.broadcast('%s joined room %s' % (user, room_name))

    return Response(
        '{"status": "OK", "message": "user joined room %s"}' % room_name,
        mimetype='text/json')


@bp.route('/leave')
def leave():
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby"}',
            mimetype='text/json')

    user = username(session)
    room = user_room(user)

    if not room:
        lobby.error('You are not in a room', dest=user, standalone=True)
        return Response(
            '{"status": "ERROR", "message": "user not in a room"}',
            mimetype='text/json')

    drop_user_from_room(room, user)

    return Response(
        '{"status": "OK", "message": "user left room %s"}' % room['name'],
        mimetype='text/json')


@bp.route('/drop/<room_name>')
def drop(room_name):
    if not rooms.get(room_name, None):
        lobby.error(
            '%s: room does not exist' % room_name,
            dest=username(session),
            standalone=True)
        return Response(
            '{"status": "ERROR", "message": "room does not exist"}',
            mimetype='text/json')

    del rooms[room_name]

    lobby.broadcast('room %s has been dropped' % room_name, standalone=True)

    return Response(
        '{"status": "OK", "message": "room dropped: %s"}' % room_name,
        mimetype='text/json')
