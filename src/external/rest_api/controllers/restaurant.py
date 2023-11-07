from flask import Blueprint

from src.external.rest_api.responses import create_response
from src.external.rest_api.schemas import RestaurantSchema
from src.external.persistence.repositories import SqliteRestaurantRepository
from src.domain.app.restaurant_service import RestaurantService


blueprint = Blueprint("restaurant", __name__)


@blueprint.route("/restaurants")
def get_restaurants():
    restaurant_repository = SqliteRestaurantRepository()
    restaurant_service = RestaurantService(restaurant_repository)
    restaurants = restaurant_service.get_all_restaurants()
    return create_response(restaurants, RestaurantSchema)