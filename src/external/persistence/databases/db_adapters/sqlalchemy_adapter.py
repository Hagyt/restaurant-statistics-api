from flask_sqlalchemy import SQLAlchemy

from src.external.persistence import OperationalException
from src.external.persistence import SQLALCHEMY_DATABASE_URI

sqlalchemy_db = SQLAlchemy()


class SQLAlchemyAdapter:

    def __init__(self, app):

        if app.config[SQLALCHEMY_DATABASE_URI] is not None:
            sqlalchemy_db.init_app(app)
        elif not app.config["TESTING"]:
            raise OperationalException("SQLALCHEMY_DATABASE_URI not set")


def setup_sqlalchemy(app, throw_exception_if_not_set=True):

    try:
        SQLAlchemyAdapter(app)
    except OperationalException as e:
        if throw_exception_if_not_set:
            raise e

    return app
