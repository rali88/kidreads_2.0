from marshmallow import Schema, fields

class PageSchema(Schema):
    id = fields.Int(dump_only=True)
    story_id = fields.Int(required=True)
    content = fields.Str(required=True)
    illustration = fields.Str(required=True)
    page_number = fields.Int(required=True)

class StorySchema(Schema):
    id = fields.Int(dump_only=True)
    age = fields.Int(required=True)
    topic = fields.Str(required=True)
    gender = fields.Str(required=True)
    bullet_points = fields.Str(required=True)
    characters = fields.Dict(keys=fields.Str(), values=fields.Str(), dump_only=True)
    pages = fields.List(fields.Nested(PageSchema), dump_only=True)
