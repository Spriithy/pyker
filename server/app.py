from flask import Flask
import os
import conn, state, lobby

app = Flask(__name__)
app.secret_key = b'q\xc1\x8f\xaf\xb2\tT\x07I\xc7%\x96\xbf\xffJ\x15'
app.register_blueprint(conn.bp)
app.register_blueprint(state.bp)
app.register_blueprint(lobby.bp)
