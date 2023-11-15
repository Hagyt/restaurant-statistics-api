from flask import Flask

from src.external.rest_api import setup_blueprints


def create_app():
    app = Flask(__name__.split('.')[0])
    app = setup_blueprints(app)
    return app