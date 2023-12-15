from marshmallow import Schema, fields

from .restaurant import RestaurantSchema


class PaginatedRestaurants(Schema):

    otal = fields.Int()
    page = fields.Int()
    per_page = fields.Int()
    items = fields.List(fields.Nested(RestaurantSchema))