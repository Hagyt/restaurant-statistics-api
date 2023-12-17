from abc import ABC, abstractmethod
from typing import List

from src.domain.model.restaurant import Restaurant


class RestaurantRepository(ABC):
    @abstractmethod
    def create(self, restaurant: Restaurant) -> Restaurant:
        pass

    
    @abstractmethod
    def update(self, object_id: str, data: dict) -> Restaurant:
        pass

    
    @abstractmethod
    def delete(self, object_id: str) -> Restaurant:
        pass


    @abstractmethod
    def get_all(self, query_params: dict = None) -> dict:
        pass
