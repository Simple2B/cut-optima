from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    SubmitField,
    SelectField,
    IntegerField,
    BooleanField,
    StringField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Email, Optional
import phonenumbers

import app.models as m


class SettingsForm(FlaskForm):
    metric_system = SelectField(
        "Metric System",
        [DataRequired()],
        choices=[(choice.name, choice.value) for choice in m.User.MetricSystem],
    )
    print_price = FloatField(
        "Price per square",
        render_kw={
            "placeholder": "0.0",
        },
        default=0.0,
    )
    currency = SelectField(
        "Currency",
        [DataRequired()],
        choices=[(choice.name, choice.value) for choice in m.User.Currency],
    )
    is_price_per = SelectField(
        "Price per",
        [DataRequired()],
        choices=[("Sheet", "Sheet"), ("Square", "Square")],
    )
    moq = IntegerField(
        "Minimum SQR order quantity",
        render_kw={
            "placeholder": "0",
        },
        default=1,
    )
    cut_spacing = FloatField(
        "Cut spacing",
        render_kw={
            "placeholder": "0.0",
        },
        default=0.5,
    )
    is_enabled_buy_btn = BooleanField(
        "Enable buy button",
        default=False,
    )
    buy_url = StringField(
        "Buy URL",
        validators=[Length(max=256)],
        render_kw={"placeholder": "e.g. https://your-site.com/buy"},
    )
    shop_name = StringField(
        "Printshop name",
        validators=[Length(max=64)],
        render_kw={"placeholder": "Amazingtransfers"},
    )
    contact_name = StringField(
        "User's name",
        validators=[Length(max=64)],
        render_kw={"placeholder": "Your name"},
    )
    contact_email = StringField(
        "User's email",
        validators=[
            Optional(),
            Email(message="Wrong email format", allow_empty_local=True),
        ],
        render_kw={"placeholder": "Your email"},
    )
    contact_phone = StringField(
        "User's phone",
        validators=[Length(max=18)],
        render_kw={"placeholder": "Your phone"},
    )

    submit = SubmitField("Save Settings")

    def validate_shop_name(form, shop_name):
        if shop_name.data and shop_name.data.isnumeric():
            raise ValidationError("Printshop name cannot be number")

    def validate_user_phone(self, phone):
        if not phone.data:
            return
        try:
            phone = phone.data
            if phone[0] != "+":
                phone = "+" + phone
            phone = phonenumbers.parse(phone)
            if not phonenumbers.is_possible_number(phone):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError("Invalid phone number")
