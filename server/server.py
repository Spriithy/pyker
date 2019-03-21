from flask import *
from uuid import uuid4
import os

app = Flask('pyker_server')
app.secret_key = os.urandom(16)
app.prefix = '/v0'


@app.route(app.prefix)
def v0():
    return 'pyker_server'


@app.route(app.prefix + '/conn/ping')
def v0_ping():
    return


@app.route(app.prefix + '/conn/init/<ip>/<int:port>')
def v0_conn_init(ip, port):
    client_id = str(uuid4())
    session[client_id] = {"ip": ip, "port": port, "client_id": client_id}
    return Response(
        '{"status": "OK", "message": "client registered", "client_id": "%s"}' %
        client_id,
        mimetype='text/json')


@app.route(app.prefix + '/conn/drop')
def v0_conn_drop():
    return
