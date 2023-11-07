from marshmallow import Schema, fields


class RestaurantSchema(Schema):
    
    id = fields.Str()
    rating = fields.Int()
    name = fields.Str()
    site = fields.Str()   
    email = fields.Str() 
    phone = fields.Str() 
    street = fields.Str() 
    city = fields.Str()
    state = fields.Str() 
    lat = fields.Float()
    lng = fields.Float()