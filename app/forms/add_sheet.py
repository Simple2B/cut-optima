from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, ValidationError
from wtforms.validators import DataRequired


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
