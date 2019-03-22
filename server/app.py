from flask import Flask
import os
import conn, state, lobby

app = Flask(__name__)
app.secret_key = os.urandom(16)
app.register_blueprint(conn.bp)
app.register_blueprint(state.bp)
app.register_blueprint(lobby.bp)
