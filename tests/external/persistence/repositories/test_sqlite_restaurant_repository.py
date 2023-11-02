from unittest import TestCase

import pandas as pd

from src.domain.model import Restaurant
from src.external.persistence.repositories import SqliteRestaurantRepository


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

        
    