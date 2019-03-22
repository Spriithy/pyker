from flask import (Blueprint, Response, request, session)

bp = Blueprint('conn', __name__, url_prefix='/v0/conn')


@bp.route('/init', methods=['POST'])
def init():
    if request.method == 'POST':
        session['ip'] = request.form.get('ip', None)
        session['user.name'] = request.form.get('user.name', None)
        if not session['user.name']:
            return Response(
                '{"status": "ERROR", "message": "username not set"}',
                mimetype='text/json')
        return Response(
            '{"status": "OK", "message": "connection established"}',
            mimetype='text/json')


@bp.route('/drop')
def drop():
    session.clear()
    return Response(
        '{"status": "OK", "message": "connection dropped"}',
        mimetype='text/json')
