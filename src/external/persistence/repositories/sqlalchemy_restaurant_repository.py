from sqlalchemy.exc import SQLAlchemyError

from src.domain.model import Restaurant
from src.external.persistence.models import RestaurantModel
from src.external.persistence.databases import sqlalchemy_db as db


class SqlalchemyRestaurantRepository:
    base_class = RestaurantModel
    DEFAULT_NOT_FOUND_MESSAGE = "Restaurant model was not found"


    def create(self, restaurant: Restaurant):
        try:
            created_object = self.base_class(**restaurant)
            db.session.add(created_object)
            db.session.commit()
            return created_object
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception("Error creating object in database")

