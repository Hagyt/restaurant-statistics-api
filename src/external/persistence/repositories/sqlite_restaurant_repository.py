from typing import List
import sqlite3

from shapely.geometry import Point

from src.domain import INSIDE_CIRCLE_SEARCH
from src.domain.model.restaurant import Restaurant
from src.domain.app.interfaces.restaurant_repository import RestaurantRepository

class SqliteRestaurantRepository(RestaurantRepository):
    
    def __init__(self) -> None:
        try:
            self.conn = sqlite3.connect('restaurants.sqlite')
            self._create_or_recreate_table_if_exists()
        except sqlite3.Error as e:
            print(e)
            raise e


    def create(self, restaurant: Restaurant) -> Restaurant:
        # Set sql to insert a restaurant
        sql = """
        INSERT INTO restaurant(
            id,
            rating,
            name,
            site,
            email,
            phone,
            street,
            city,
            state,
            lat,
            lng
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """

        try:
            # Set values to insert
            data = (
                restaurant.id,
                restaurant.rating,
                restaurant.name,
                restaurant.site,
                restaurant.email,
                restaurant.phone,
                restaurant.street,
                restaurant.city,
                restaurant.state,
                restaurant.lat,
                restaurant.lng
            )
            # Set cursor and execute the sql to insert the new restaurant
            cursor = self.conn.cursor()
            cursor.execute(sql, data)
            self.conn.commit()

            return restaurant
        except Exception as e:
            print(e)
            raise e
        
    
    def update(self, object_id: str, data: dict) -> Restaurant:
        # Set query to update a restaurant
        sql = """
        UPDATE restaurant
            SET rating = ?,
                name = ?,
                site = ?,
                email = ?,
                phone = ?,
                street = ?,
                city = ?,
                state = ?,
                lat = ?,
                lng = ?
            WHERE id = ?
        """
        try:
            restaurant = Restaurant(
                data.get("rating"),
                data.get("name"),
                data.get("site"),
                data.get("email"),
                data.get("phone"),
                data.get("street"),
                data.get("city"),
                data.get("state"),
                data.get("lat"),
                data.get("lng"),
                object_id
            )
            # Set values to insert
            data = (
                restaurant.rating,
                restaurant.name,
                restaurant.site,
                restaurant.email,
                restaurant.phone,
                restaurant.street,
                restaurant.city,
                restaurant.state,
                restaurant.lat,
                restaurant.lng,
                restaurant.id,
            )

            # Set cursor and execute the insert the new restaurant
            cursor = self.conn.cursor()
            cursor.execute(sql, data)
            self.conn.commit()

            return restaurant
        except Exception as e:
            print(e)
            raise e
    
    
    def delete(self, object_id: str) -> Restaurant:
        # Set query to delete a restaurant
        delete_sql = "DELETE FROM restaurant WHERE id = ?"
        find_by_id_sql = "SELECT * FROM restaurant WHERE id = ?"

        try:
            # Set cursor and execute the sql to find by id
            cursor = self.conn.cursor()
            data = cursor.execute(find_by_id_sql, [object_id]).fetchone()

            if data is None:
                raise Exception("Not found")

            restaurant = Restaurant(
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[0]
            )
            cursor.execute(delete_sql, (object_id,))
            self.conn.commit()
            
            return restaurant
        except Exception as e:
            print(e)
            raise e

    def get_all(self, query_params: dict = None) -> List[Restaurant]:
        # Set query to get all restaurants
        query = "SELECT * FROM restaurant"

        try:
            # Set cursor and execute the query
            cursor = self.conn.cursor()
            data = cursor.execute(query).fetchall()

            # Get the restaurants from data and set it into a list
            restaurants = [
                Restaurant(
                    id=row[0],
                    rating=row[1],
                    name=row[2],
                    site=row[3],
                    email=row[4],
                    phone=row[5],
                    street=row[6],
                    city=row[7],
                    state=row[8],
                    lat=row[9],
                    lng=row[10]
                )

                for row in data
            ]

            restaurants = self._apply_query_params(query_params)

            return restaurants
        except Exception as e:
            print(e)
            raise e
        
    
    def _apply_query_params(self, restaurants: List[Restaurant], query_params: dict) -> List[Restaurant]:

        if query_params is None:
            filtered_restaurants = restaurants.copy()
        
        function_query_param = query_params.get("function")

        if function_query_param == INSIDE_CIRCLE_SEARCH:
            radius_query_param = query_params.get("radius")
            center_query_param = query_params.get("center_point")

            filtered_restaurants = [
                r for r in restaurants 
                if self._is_inside_circle(center_query_param, radius_query_param)
            ]
            

        return filtered_restaurants
    

    def _is_inside_circle(restaurant: Restaurant, center_point: Point, radius: float):
        # Calculate distances and determine if it is inside
        lat = center_point.y
        lng = center_point.x
        return pow((float(restaurant.lat[9]) - lat), 2) + pow((float(restaurant.lng) - lng), 2) <= radius
    
    def _create_or_recreate_table_if_exists(self):
        # Open cursor
        cursor = self.conn.cursor()
        # Set and execute query to drop table if it exists
        drop_table_query = """
        DROP TABLE IF EXISTS restaurant
        """
        cursor.execute(drop_table_query)

        # Set query to create restaurant table
        create_table_query = """
        CREATE TABLE restaurant(
            id text PRIMARY_KEY,
            rating integer NOT NULL,
            name text NOT NULL,
            site text NOT NULL,
            email text NOT NULL,
            phone text NOT NULL,
            street text NOT NULL,
            city text NOT NULL,
            state text NOT NULL,
            lat real NOT NULL,
            lng real NOT NULL
        )
        """
        cursor.execute(create_table_query)
