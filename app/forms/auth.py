from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, EmailField
from wtforms.validators import DataRequired, Length, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    email = EmailField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(2, 30)])
    email = EmailField("Email Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 30)])
    password_confirmation = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Password do not match."),
        ],
    )
    submit = SubmitField("Register")

    def validate_username(form, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError("This username is taken.")

    def validate_email(form, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError("This email is already registered.")


class ForgotPassword(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Length(max=256)],
        render_kw={"placeholder": "Email"},
    )
    submit = SubmitField("Reset Password")

    def validate_email(form, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Email not found")
