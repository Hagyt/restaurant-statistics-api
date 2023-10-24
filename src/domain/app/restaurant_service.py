from typing import List

from shapely.geometry import Point

from src.domain.model import Restaurant
from src.domain.app.interfaces import RestaurantRepository


class RestaurantService:

    def __init__(self, restaurant_repository: RestaurantRepository) -> None:
        self.restaurant_repository = restaurant_repository


    def get_all_restaurants(self) -> List[Restaurant]:
        return self.restaurant_repository.get_all()


    def create_restaurant(self, data: dict) -> Restaurant:
        new_restaurant = Restaurant(**data)
        return self.restaurant_repository.create(new_restaurant)


    def update_restaurant(self, data: dict) -> Restaurant:
        restaurant_update = Restaurant(**data)
        return self.restaurant_repository.update(restaurant_update)


    def remove_restaurant(self, restaurant_id: str) -> Restaurant:
        return self.restaurant_repository.delete(restaurant_id)
    

    def get_area_restaurants_statistics(self, lat: float, long: float, radius: float) -> dict:
        ## Create a Shapely Point object representing the circle's center
        circle_center = Point(long, lat)

        ## Set query params for the inquiry to the repository
        query_params = {
            'function': 'ST_DWithin',
            'center_point': circle_center,
            'radius': radius
        }
        return self.restaurant_repository.get_all(query_params)
        