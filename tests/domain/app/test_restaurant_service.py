from unittest import TestCase

import pandas as pd

from src.domain.model import Restaurant
from src.domain.app import RestaurantService
from src.external.persistence.repositories import SqliteRestaurantRepository



class TestRestaurantService(TestCase):

    def setUp(self) -> None:
        restaurant_repository = SqliteRestaurantRepository()
        self.restaurant_service = RestaurantService(restaurant_repository)

        try:
            cursor = restaurant_repository.conn.cursor()
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
                    restaurant_repository.conn.commit()
                else:
                    print('There is already a restaurant with the id')
        except Exception as e:
            print(e)


    def test_get_all_restaurants(self):
        number_total_restaurants = 100
        restaurants = self.restaurant_service.get_all_restaurants()
        self.assertIsInstance(restaurants, list)
        self.assertEqual(len(restaurants), number_total_restaurants)