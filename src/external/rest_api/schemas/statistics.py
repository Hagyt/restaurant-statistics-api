from marshmallow import Schema, fields


class StatisticsSchema(Schema):

    count = fields.Int()
    avg = fields.Float()
    std = fields.Float()