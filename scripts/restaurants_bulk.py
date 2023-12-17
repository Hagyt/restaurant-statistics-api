"""
This script insert the data stored in resources 
to the SQL database to test the api.

This script must be executed only once.

"""

import os

import pandas as pd
from sqlalchemy import text
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

engine = create_engine(os.environ.get("SQLALCHEMY_DATABASE_URI"), echo=True)

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
) VALUES (:id,
    :rating,
    :name,
    :site,
    :email,
    :phone,
    :street,
    :city,
    :state,
    :lat,
    :lng)
"""


with engine.begin() as conn:
    result = conn.execute(text(insert_sql), df.to_dict('records'))
    