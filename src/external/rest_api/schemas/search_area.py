from marshmallow import Schema, fields


class SearchAreaSchema(Schema):

    latitude = fields.Float()
    longitude = fields.Float()
    radius = fields.Float()