from flask import Blueprint

from src.external.rest_api.middleware import post_data_required
from src.external.rest_api.responses import create_response
from src.external.rest_api.schemas import RestaurantSchema
from src.external.persistence.repositories import SqliteRestaurantRepository
from src.domain.app.restaurant_service import RestaurantService


blueprint = Blueprint("restaurant", __name__)


@blueprint.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurant_repository = SqliteRestaurantRepository()
    restaurant_service = RestaurantService(restaurant_repository)
    restaurants = restaurant_service.get_all_restaurants()
    return create_response(restaurants, RestaurantSchema)


@blueprint.route("/restaurants", methods=["POST"])
@post_data_required
def save_restaurant(json_data):
    # Validate data
    restaurant_schema = RestaurantSchema()
    validated_data = restaurant_schema.load(json_data)

    # Create restaurant using service
    restaurant_repository = SqliteRestaurantRepository()
    restaurant_service = RestaurantService(restaurant_repository)
    restaurant_created = restaurant_service.create_restaurant(validated_data)    
    return create_response(restaurant_created, RestaurantSchema)


@blueprint.route("/restaurants/<string:id>", methods=["PUT"])
@post_data_required
def update_restaurant(json_data, id):
    # Validate data
    json_data["id"] = id
    restaurant_schema = RestaurantSchema()
    validated_data = restaurant_schema.load(json_data)

    # Update restaurant using service
    restaurant_repository = SqliteRestaurantRepository()
    restaurant_service = RestaurantService(restaurant_repository)
    print(validated_data)
    restaurant_updated = restaurant_service.update_restaurant(validated_data)
    return create_response(restaurant_updated, RestaurantSchema)