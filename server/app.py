from flask import Flask
import os
import conn

app = Flask(__name__)
app.secret_key = os.urandom(16)
app.register_blueprint(conn.bp)
