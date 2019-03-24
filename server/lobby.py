from flask import *
import json
from conn import username
import datetime
import state

bp = Blueprint('lobby', __name__, url_prefix='/v0/lobby')


def error(message, dest='lobby'):
    broadcast(message, dest=dest, level='ERROR')


def warning(message, dest='lobby'):
    broadcast(message, dest=dest, level='WARNING')


def broadcast(message, dest='lobby', level='INFO'):
    messages.append({
        "id": len(messages),
        "from": level,
        "to": dest,
        "date": datetime.datetime.now().strftime('%H:%M:%S'),
        "content": message,
    })


messages = []


@bp.route('/join')
def join():
    broadcast('Welcome on Pyker!', dest=username(session))
    return Response('{"status": "OK", "message": ""}')


@bp.route('/last_message_id')
def last_message_id():
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby"}',
            mimetype='text/json')

    return Response(
        '{"status": "OK", "message": "", "payload.type": "int", "int": %d}' %
        len(messages),
        mimetype='text/json')


@bp.route('/pull/messages')
def pull_messages():
    """
    
    method: GET
    args:   start: l'id du dernier message recu
    
    """
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby"}',
            mimetype='text/json')

    start = 0
    if request.args.get('start', None):
        start = int(request.args.get('start'))
    user = session['user.name'] + '#' + session['user.id']
    local_messages = list(
        filter(
            lambda m: m['from'] == user or m['to'] == 'lobby' or m['to'] ==
            user, messages[start:]))
    return Response(
        '{"status":"OK", "message":"", "payload.type": "lobby.messages", "lobby.messages": '
        + json.dumps(local_messages) + '}',
        mimetype='text/json')


@bp.route('/pull/whispers/<from_user>')
def pull_whispers(from_user):
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby"}',
            mimetype='text/json')

    user = session['user.name'] + '#' + session['user.id']
    local_messages = list(
        filter(
            lambda m: (m['from'] == user or m['to'] == from_user) and (m[
                'to'] == from_user or m['from'] == user), messages))
    return Response(
        '{"status":"OK", "message":"", "payload.type": "whispers.messages", "whispers.messages": '
        + json.dumps(local_messages) + '}',
        mimetype='text/json')


@bp.route('/push/message', methods=['POST'])
def push_message():
    """

    method: POST
    form:   message.to:   destinataire du message (ex: Spriithy#2367)
            message.from: celui qui a envoyé le message (ex: ErnestBidouille#8888)

    """
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby"}',
            mimetype='text/json')

    content = request.form.get('message.content', '')

    message = {
        "id": len(messages),
        "from": session['user.name'] + '#' + session['user.id'],
        "to": request.form.get('message.to', 'lobby'),
        "date": datetime.datetime.now().strftime('%H:%M:%S'),
        "content": content,
    }
    messages.append(message)
    return Response(
        '{"status": "OK", "message": "", "payload.type": "lobby.messages", "lobby.messages": '
        + json.dumps([message]) + '}',
        mimetype='text/json')
