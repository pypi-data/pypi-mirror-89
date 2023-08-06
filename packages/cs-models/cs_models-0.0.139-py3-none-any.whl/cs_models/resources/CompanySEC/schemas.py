from marshmallow import (
    Schema,
    fields,
    validate,
)


class CompanySECResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    cik_str = fields.String(required=True, validate=not_blank)
    ticker = fields.String(allow_none=True)
    title = fields.String(required=True)
    updated_at = fields.DateTime(dump_only=True)
