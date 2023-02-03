from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    StringField,
    ValidationError,
    TextAreaField,
)
from wtforms.validators import Length, Email


class FeedbackForm(FlaskForm):
    feedback_name = StringField(
        "Name",
        validators=[Length(max=15)],
        render_kw={"placeholder": "Your Name"},
    )
    feedback_email = StringField(
        "Email",
        validators=[Email(message="Wrong email format")],
        render_kw={"placeholder": "Email"},
    )
    feedback_message = TextAreaField(
        "Feedback message",
        validators=[Length(max=640)],
        render_kw={"placeholder": ""},
    )

    submit = SubmitField("Leave Feedback")
