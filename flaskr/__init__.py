from flask import Flask
from api import v1

app = Flask(__name__)

app.register_blueprint(v1.api, url_prefix = "/api/v1")
