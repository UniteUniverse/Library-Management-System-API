from marshmallow import Schema, fields, validate

# Book Schema
class BookSchema(Schema):
    id = fields.Int(dump_only=True)  # 'id' is read-only
    title = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    published_year = fields.Int()
    isbn = fields.Str(required=True, validate=validate.Length(min=10, max=20))

# Member Schema
class MemberSchema(Schema):
    id = fields.Int(dump_only=True)  # 'id' is read-only
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)  # Validates email format
    join_date = fields.Date(required=True)
