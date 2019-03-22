from flask import *
import json

import datetime
import state

bp = Blueprint('lobby', __name__, url_prefix='/v0/lobby')

messages = [{
    "id": 0,
    "from": "server",
    "to": "lobby",
    "date": "00:00:00",
    "content": "Welcome on Pyker!"
}]


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
    if content[0] in ['.', '!', '/']:
        return Response(
            '{"status": "ERROR", "message": "commands not implemented"}',
            mimetype='text/json')

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
