import pandas as pd
from sqlalchemy import inspect
from flask_migrate import Migrate

from src.external.persistence.databases import sqlalchemy_db as db
from src.external.persistence.repositories import SqlalchemyRestaurantRepository


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


    @app.cli.command("bulk_seed_restaurant_data")
    def bulk_seed_restaurant_data():
        restaurant_repository = SqlalchemyRestaurantRepository()
        ## Read csv
        df = pd.read_csv("resources/restaurantes.csv")

        ## Create geom property
        def create_geom_property(row):
            row["geom"] = {
                "lng": row["lng"],
                "lat": row["lat"]
            }
            return row
        
        data = list(map(create_geom_property, df.to_dict("records")))
        
        for r in data:
            restaurant_created = restaurant_repository.create(r)
            print(f"Restaurant created: {restaurant_created.__str__()}")
        
    return app