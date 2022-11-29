from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired

from app.models import Sheet


class AddSheet(FlaskForm):
    width = FloatField(
        "Width",
        [DataRequired()],
    )
    height = FloatField(
        "Height",
        [DataRequired()],
    )

    submit = SubmitField("Add Sheet")

    def validate_width(form, width):
        if width.data <= 0:
            raise ValidationError("Width cannot be 0 or less")

    def validate_height(form, height):
        if height.data <= 0:
            raise ValidationError("Height cannot be 0 or less")


class DeleteSheet(FlaskForm):
    id = IntegerField(
        "Sheet Id",
        [DataRequired()],
    )

    submit = SubmitField("Delete Sheet")

    def validate_id(form, id):
        if not Sheet.query.get(id.data):
            raise ValidationError("Sheet not found")
