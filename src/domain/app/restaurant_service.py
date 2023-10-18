from typing import List

from src.domain.model.restaurant import Restaurant
from src.domain.app.interfaces.restaurant_repository import RestaurantRepository


class RestaurantService:

    def __init__(self, restaurant_repository: RestaurantRepository) -> None:
        self.restaurant_repository = restaurant_repository


    def get_all_restaurants(self) -> List[Restaurant]:
        return self.restaurant_repository.get_all()


    def create_restaurant(self, data: dict) -> Restaurant:
        new_restaurant: Restaurant = Restaurant(**data)
        return self.restaurant_repository.create(new_restaurant)


    def update_restaurant(self) -> Restaurant:
        pass


    def remove_restaurant(self) -> Restaurant:
        pass
    

    def get_area_restaurants_statistics(self) -> dict:
        pass
        