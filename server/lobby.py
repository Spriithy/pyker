import json
from flask import *

bp = Blueprint('lobby', __name__, url_prefix='/v0/lobby')

messages = [{
    "from": "server",
    "date": "00:00:00 01/01/2019",
    "content": "hello",
}]


@bp.route('/get/messages')
def get_messages(start=0):
    if request.args.get('start', None):
        start = int(request.args.get('start'))
    return Response(
        '{"status":"OK", "message":"", "payload.type": "lobby.messages", "lobby.messages": '
        + json.dumps(messages[start:]) + '}',
        mimetype='text/json')
