from flask import (Blueprint, Response, request, session)
from uuid import uuid4
import state

bp = Blueprint('conn', __name__, url_prefix='/v0/conn')


@bp.route('/init', methods=['POST'])
def init():
    if request.method == 'POST':
        session['user.name'] = request.form.get('user.name', None)
        session['user.id'] = str(uuid4())
        session['state'] = state.NO_LOBBY
        if not session['user.name']:
            return Response(
                '{"status": "ERROR", "message": "username not set"}',
                mimetype='text/json')
        return Response(
            '{"status": "OK", "message": "connection established", "user.id": "%s"}'
            % session['user.id'],
            mimetype='text/json')


@bp.route('/drop')
def drop():
    session.clear()
    return Response(
        '{"status": "OK", "message": "connection dropped"}',
        mimetype='text/json')
