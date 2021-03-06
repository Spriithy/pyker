from flask import *

bp = Blueprint('state', __name__, url_prefix='/v0')

NO_LOBBY = 0
IN_LOBBY = 1


@bp.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == 'GET':
        if session['state'] == NO_LOBBY:
            session['state'] = IN_LOBBY
            return Response(
                '{"status": "OK", "message":"", "action": "lobby.join"}',
                mimetype='text/json')
    return ''
