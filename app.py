# Flask, request, jsonfy
from flask import Flask, request, jsonify

# sqlite3
import sqlite3

# models
from models import Restaurant

# db
from db import db_connection

app = Flask(__name__)

@app.route('/restaurants')
def get_restaurants():
    # Connect to db
    conn = db_connection()
    # Set query to get all restaurants
    query = "SELECT * FROM restaurant"

    try:
        # Set cursor and execute the query
        cursor = conn.cursor()
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
            ).__dict__

            for row in data
        ]

        # Check if there are restaurants
        if len(restaurants) > 0:
            return jsonify(restaurants)
        else:
            return jsonify({ 'message': 'It seems Its empty :o' }), 404
    except Exception as e:
        print(e)
        return jsonify({ 'message': 'Im sorry, Something went wrong :('})

    
@app.route('/restaurants', methods=['POST'])
def save_restaurant():
    # Connect to db
    conn = db_connection()

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
        # Create a restaurant object
        restaurant = Restaurant(
            rating=request.json['rating'],
            name=request.json['name'],
            site=request.json['site'],
            email=request.json['email'],
            phone=request.json['phone'],
            street=request.json['street'],
            city=request.json['city'],
            state=request.json['state'],
            lat=request.json['lat'],
            lng=request.json['lng']
        )

        # Generate a objectID to assing it to the new restaurant
        restaurant.set_generated_id()
        
        # Parse restaurant values to tuple
        data = tuple(restaurant.__dict__.values())

        # Set cursor and execute the sql to insert the new restaurant
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()

        # Response to client
        return jsonify({ 'message': 'Restaurant created successfully', 
                            'id': restaurant.id
                        }), 200
    except Exception as e:
        print(e)
        return jsonify({ 'message': 'Im sorry, something went wrong :o' }), 500

@app.route('/restaurants/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def single_restaurant(id):
    # Connect to db
    conn = db_connection()

    if request.method == 'GET':
        # Set query to get a specific restaurant
        query = "SELECT * FROM restaurant WHERE id = ?"
        restaurant = None

        try:
            # Set cursor and execute the query
            cursor = conn.cursor()
            data = cursor.execute(query, [id]).fetchall()

            restaurant = [
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

            if 0 < len(restaurant) < 2:
                return jsonify(restaurant[0].__dict__)
            elif len(restaurant) == 0:
                return jsonify({ 'message': 'It seems it does not exist :o' }), 404
            else:
                return jsonify({ 'message': 'Im sorry, something went wrong :o' }), 500
        except Exception as e:
            print(e)
            return jsonify({ 'message': 'Im sorry, something went wrong :o' }), 500
    
    if request.method == 'PUT':
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
            # Create a restaurant object
            restaurant = Restaurant(
                id=id,
                rating=request.json['rating'],
                name=request.json['name'],
                site=request.json['site'],
                email=request.json['email'],
                phone=request.json['phone'],
                street=request.json['street'],
                city=request.json['city'],
                state=request.json['state'],
                lat=request.json['lat'],
                lng=request.json['lng']
            )

            # Restructure restaurant values order to execute update
            data = list(restaurant.__dict__.values())
            data = data[1:]
            data.append(id)
            data = tuple(data)

            # Set cursor and execute the insert the new restaurant
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()

            # Response to client
            return jsonify({ 
                             'message': 'Restaurant updated successfully', 
                             'restaurant': restaurant.__dict__
                           }), 200
        except Exception as e:
            print(e)
            return jsonify({ 'message': 'Im sorry, something went wrong :o' }), 500

    if request.method == 'DELETE':
        # Set query to delete a restaurant
        sql = "DELETE FROM restaurant WHERE id = ?"

        try:
            # Set cursor and execute the insert the new restaurant
            cursor = conn.cursor()
            cursor.execute(sql, [id])
            conn.commit()
            
            # Response to client
            return jsonify({ 
                             'message': 'Restaurant deleted successfully',
                             'id': id
                           })
        except Exception as e:
            print(e)
            return jsonify({ 'message': 'Im sorry, something went wrong :o' }), 500

if __name__ == '__main__':
    app.run(debug=True)