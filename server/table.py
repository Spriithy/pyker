from flask import *
import json
import random
import lobby
import state

bp = Blueprint('table', __name__, url_prefix='/table')

tables = {}


def user_table(user):
    for table in tables:
        if table['users'].index(user) >= 0:
            return table

    return None


@bp.route('/list')
def list_tables():
    return Response(
        '{"status": "OK", "message": "", "payload.type": "table.list", "table.list": '
        + json.dumps(list(filter(lambda t: tables[t]['table.name'],
                                 tables))) + '}',
        mimetype='text/json')


@bp.route('/init', methods=['POST'])
def init():
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby"}',
            mimetype='text/json')
    user = '%s#%s' % (session['user.name'], session['user.id'])
    table_id = str(random.randint(0, 1000))
    table_name = request.form.get('table.name', 'table#%s' % table_id)
    tables[table_name] = {
        "table.name": table_name,
        "table.id": table_id,
        "table.users": [user],
    }

    lobby.broadcast('%s created table %s' % (user, table_name))

    return Response(
        '{"status": "OK", "message": "table created", "table.name": "%s", "table.id": "%s"}'
        % (table_name, table_id),
        mimetype='text/json')


@bp.route('/join/<table_name>')
def join(table_name):
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby"}',
            mimetype='text/json')

    user = '%s#%s' % (session['user.name'], session['user.id'])

    if user_table(user):
        return Response(
            '{"status": "ERROR", "message": "user already on a table"}',
            mimetype='text/json')

    if not tables.get(table_name, None):
        return Response(
            '{"status": "ERROR", "message": "no such table %s"}' % table_name,
            mimetype='text/json')

    tables[table_name]['users'].append(user)

    lobby.broadcast('%s joined table %s' % (user, table_name))

    return Response(
        '{"status": "OK", "message": "user joined table %s"}' % table_name,
        mimetype='text/json')


@bp.route('/leave')
def leave():
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby"}',
            mimetype='text/json')

    user = '%s#%s' % (session['user.name'], session['user.id'])
    table = user_table(user)

    if not table:
        return Response(
            '{"status": "ERROR", "message": "user not on a table"}',
            mimetype='text/json')

    user = '%s#%s' % (session['user.name'], session['user.id'])
    table['users'].remove(user)

    lobby.broadcast('%s left table %s' % (user, table['table.name']))

    return Response(
        '{"status": "OK", "message": "user left table: %s"}' %
        table['table.name'],
        mimetype='text/json')


@bp.route('/drop/<table_name>')
def drop(table_name):
    if not tables.get(table_name, None):
        return Response(
            '{"status": "ERROR", "message": "table does not exist"}',
            mimetype='text/json')

    del tables[table_name]

    return Response(
        '{"status": "OK", "message": "table dropped: %s"}' % table_name,
        mimetype='text/json')
