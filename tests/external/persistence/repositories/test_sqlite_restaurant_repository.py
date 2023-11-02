from typing import List
from unittest import TestCase

import pandas as pd
from shapely.geometry import Point

from src.domain.model import Restaurant
from src.external.persistence.repositories import SqliteRestaurantRepository
from src.domain import INSIDE_CIRCLE_SEARCH


class TestSqliteRestaurantRepository(TestCase):

    def setUp(self) -> None:
        self.repository = SqliteRestaurantRepository()

        try:
            cursor = self.repository.conn.cursor()
            # Read csv
            data = pd.read_csv('resources/restaurantes.csv')

            # Set data as DataFrame
            df = pd.DataFrame(data)

            # Set query to verify if restaurant exists
            select_query = """
            SELECT * FROM restaurant WHERE id = ?
            """

            # Set query to insert data
            insert_sql = """
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

            for index, row in df.iterrows():
                # Get values
                id = row['id']
                rating = row['rating']
                name = row['name']
                site = row['site']
                email = row['email']
                phone = row['phone']
                street = row['street']
                city = row['city']
                state = row['state']
                lat = row['lat']
                lng = row['lng']

                restaurant = cursor.execute(select_query, [id]).fetchone()

                if restaurant is None:

                    # Set values as tuple
                    values = (
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
                    )

                    # Execute sql
                    cursor.execute(insert_sql, values)

                    # Commit the transaction
                    self.repository.conn.commit()
                else:
                    print('There is already a restaurant with the id')
        except Exception as e:
            print(e)

        
    def test_create_restaurant(self):
        restaurant = Restaurant(
            1,
            "New_Test_Restaurant",
            "https://site.fake.com",
            "email.fake@test.com",
            "534845201",
            "44545e Fake street",
            "City_Fake",
            "Fake_State",
            19.4400570537131,
            -98.1270470974249,
            "1",
        )

        restaurant_created = self.repository.create(restaurant)
        self.assertIsInstance(restaurant_created, Restaurant)

    
    def test_update_restaurant(self):
        restaurant_id = "edb50561-46f9-4541-9c04-8de82401cc13"
        restaurant_data = {
            "rating": 1,
            "name": "New_Test_Restaurant_2",
            "site": "https://site.fake2.com",
            "email": "email.fake2@test.com",
            "phone": "534845201 E 2",
            "street": "44545e Fake street2",
            "city": "City_Fake2",
            "state": "Fake_State2",
            "lat": 19.4400570537132,
            "lng": -98.1270470974242
        }
        restaurant_updated = self.repository.update(restaurant_id, restaurant_data)
        self.assertIsInstance(restaurant_updated, Restaurant)

        
    def test_delete_restaurant(self):
        restaurant_id = "edb50561-46f9-4541-9c04-8de82401cc13"
        # restaurant_id = "1"
        restaurant_deleted = self.repository.delete(restaurant_id)
        self.assertIsInstance(restaurant_deleted, Restaurant)


    def test_get_all_restaurants(self):
        number_total_restaurants = 100
        restaurants = self.repository.get_all()
        self.assertIsInstance(restaurants, list)
        self.assertEqual(len(restaurants), number_total_restaurants)


    def test_get_restaurants_inside_circle(self):
        number_total_restaurants = 3
        long = -99.1313996519641
        lat = 19.4420166275981
        radius = 10
        ## Create a Shapely Point object representing the circle's center
        circle_center = Point(long, lat)

        ## Set query params for the inquiry to the repository
        query_params = {
            'function': INSIDE_CIRCLE_SEARCH,
            'center_point': circle_center,
            'radius': radius
        }
        restaurants = self.repository.get_all(query_params)
        self.assertIsInstance(restaurants, list)
        self.assertEqual(len(restaurants), number_total_restaurants)
