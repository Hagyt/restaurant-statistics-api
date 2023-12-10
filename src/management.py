from sqlalchemy import inspect
from flask_migrate import Migrate

from src.external.persistence.databases import sqlalchemy_db as db


migrate = Migrate()


def setup_management(app):
    migrate.init_app(app, db)

    @app.cli.command("show_db_tables")
    def show_db_tables():
        inspector = inspect(db.engine)
        print(inspector.get_table_names())

    
    @app.cli.command("print_config")
    def print_config():
        print(app.config)
        
    return app