from flask_wtf import FlaskForm
from wtforms import (
    FloatField,
    SubmitField,
    SelectField,
    IntegerField,
    BooleanField,
    StringField,
)
from wtforms.validators import DataRequired, Length

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
        "Minimum order quantity",
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

    submit = SubmitField("Save Settings")
