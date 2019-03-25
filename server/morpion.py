from flask import *
from conn import username
from response import *
import json
import random
import lobby
import state
from room import *

bp = Blueprint('morpion', __name__, url_prefix='/morpion')


@bp.route('/start')
def start():
    user = username(session)
    table = user_room(user)

    if not table:
        lobby.error('You are not in any room yet', dest=user, standalone=True)
        return Response(error('user not in a room'), mimetype='text/json')

    if len(table['users']) > 2:
        for user in table['users']:
            lobby.warning('Too many players to start a Tac Tac Toe game')
            return Response(
                error('too many players in room'), mimetype='text/json')

    return Response(ok())
