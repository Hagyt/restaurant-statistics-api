from flask import Flask

from src.external.rest_api import setup_blueprints
from src.external.persistence.databases import setup_sqlalchemy


def create_app(config):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)
    app = setup_blueprints(app)
    app = setup_sqlalchemy(app)
    return app