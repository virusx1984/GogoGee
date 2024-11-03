from marshmallow import Schema, fields

class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    description = fields.String(required=True)
    completed = fields.Boolean()