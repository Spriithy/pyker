from flask import *
from conn import username
import json
import random
import lobby
import state

bp = Blueprint('table', __name__, url_prefix='/v0/table')

tables = {}


def user_table(user):
    for table in tables.values():
        if user in table['users']:
            return table
    return None


def drop_user_from_table(table, user):
    table['users'].remove(user)
    lobby.broadcast('%s left table %s' % (user, table['name']))
    if len(table['users']) == 0:
        del tables[table['name']]
        lobby.broadcast(
            'table %s has been automatically removed' % table['name'],
            standalone=True)


@bp.route('/list')
def list_tables():
    return Response(
        '{"status": "OK", "message": "", "payload.type": "table.list", "table.list": '
        + json.dumps(list(map(lambda t: tables[t], tables))) + '}',
        mimetype='text/json')


@bp.route('/init', methods=['POST'])
def init():
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby"}',
            mimetype='text/json')

    user = username(session)
    table_id = str(random.randint(0, 1000))
    table_name = request.form.get('table.name', 'table#%s' % table_id)

    if tables.get(table_name, None):
        lobby.broadcast(
            'Table %s already exists' % (table_name),
            dest=username(session),
            level="Error",
            standalone=True)
        return Response(
            '{"status": "OK", "message": "table already exists", "table.name": "%s"}'
            % (table_name),
            mimetype='text/json')

    prev_table = user_table(user)
    if prev_table:
        drop_user_from_table(prev_table, user)
        lobby.warning(
            'You have automatically been removed from table %s' %
            prev_table['name'],
            dest=user,
            standalone=True)

    tables[table_name] = {
        "name": table_name,
        "id": table_id,
        "users": [user],
    }

    lobby.broadcast('%s created table %s' % (user, table_name))

    return Response(
        '{"status": "OK", "message": "table created", "table.name": "%s", "table.id": "%s"}'
        % (table_name, table_id),
        mimetype='text/json')


@bp.route('/get')
def get():
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby", "payload.type": "str", "str": ""}',
            mimetype='text/json')
    user = username(session)
    table = user_table(user)
    if table:
        return Response(
            '{"status": "OK", "message": "", "payload.type": "str", "str": "%s"}'
            % table['name'],
            mimetype='text/json')
    else:
        return Response(
            '{"status": "OK", "message": "user not in table", "payload.type": "str", "str": ""}',
            mimetype='text/json')


@bp.route('/join/<table_name>')
def join(table_name):
    if session['state'] is not state.IN_LOBBY:
        return Response(
            '{"status": "ERROR", "message": "user not in lobby"}',
            mimetype='text/json')

    user = username(session)
    prev_table = user_table(user)
    if prev_table:
        drop_user_from_table(prev_table, user)
        lobby.warning(
            'You have automatically been removed from table %s' %
            prev_table['name'],
            dest=user,
            standalone=True)

    if not tables.get(table_name, None):
        lobby.error(
            'Table %s does not exist' % table_name, dest=user, standalone=True)
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

    user = username(session)
    table = user_table(user)

    if not table:
        lobby.error('You are not on a table.', dest=user, standalone=True)
        return Response(
            '{"status": "ERROR", "message": "user not on a table"}',
            mimetype='text/json')

    drop_user_from_table(table, user)

    return Response(
        '{"status": "OK", "message": "user left table: %s"}' % table['name'],
        mimetype='text/json')


@bp.route('/drop/<table_name>')
def drop(table_name):
    if not tables.get(table_name, None):
        lobby.error(
            '%s: Table does not exist.' % table_name,
            dest=username(session),
            standalone=True)
        return Response(
            '{"status": "ERROR", "message": "table does not exist"}',
            mimetype='text/json')

    del tables[table_name]

    lobby.broadcast('table %s has been dropped' % table_name, standalone=True)

    return Response(
        '{"status": "OK", "message": "table dropped: %s"}' % table_name,
        mimetype='text/json')
