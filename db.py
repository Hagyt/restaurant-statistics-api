# sqlite3
import sqlite3

# pandas
import pandas as pd

# Function to connect to db
def db_connection():
    conn = None

    try:
        conn = sqlite3.connect('restaurants.sqlite')
    except sqlite3.Error as e:
        print(e)
    finally:
        return conn

try:
    # Connect to db
    conn = db_connection()

    # Set cursor
    cursor = conn.cursor()

    # Set  and execute query to drop table if it exists
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

    # Read csv
    data = pd.read_csv('resources/restaurantes.csv')

    # Set data as DataFrame
    df = pd.DataFrame(data)

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
        conn.commit()
except Exception as e:
    print(e)