from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

import app.models as m


class LoginForm(FlaskForm):
    email = EmailField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(2, 30)])
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")

    def validate_username(form, field):
        if m.User.query.filter_by(username=field.data).first() is not None:
            raise ValidationError("This username is taken.")

    def validate_email(form, field):
        if m.User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError("This email is already registered.")


class ForgotPassword(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Length(max=256), Email()],
        render_kw={"placeholder": "Email"},
    )
    submit = SubmitField("Reset Password")

    def validate_email(form, email):
        user = m.User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Email not found")


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        [DataRequired(), EqualTo("confirm_password", message="Passwords must match")],
        render_kw={"placeholder": "Password"},
    )
    confirm_password = PasswordField(
        "Repeat Password", render_kw={"placeholder": "Repeat Password"}
    )
    submit = SubmitField("Change password")
