from datetime import datetime
from uuid import uuid4
import enum

from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import func, Enum
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.utils import ModelMixin


def gen_password_reset_id() -> str:
    return str(uuid4())


class User(db.Model, UserMixin, ModelMixin):
    __tablename__ = "users"

    # Enums
    class MetricSystem(enum.Enum):
        centimeter = "centimeter"
        inch = "inch"

    class Currency(enum.Enum):
        dollar = "dollar"
        pound = "pound"
        euro = "euro"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    activated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    deleted = db.Column(db.Boolean, default=False)
    reset_password_uid = db.Column(db.String(64), default=gen_password_reset_id)

    # settings
    metric_system = db.Column(Enum(MetricSystem), default=MetricSystem.centimeter)
    print_price = db.Column(db.Float(), default=0)
    is_price_per_sheet = db.Column(db.Boolean, default=False)
    moq = db.Column(db.Integer(), default=1)
    cut_spacing = db.Column(db.Float(), default=0.5)
    is_enabled_buy_btn = db.Column(db.Boolean, default=False)
    buy_url = db.Column(db.String(255), nullable=True)
    currency = db.Column(Enum(Currency), default=Currency.dollar)
    shop_name = db.Column(db.String(64), nullable=True, unique=True)
    logo_img = db.Column(db.Text, nullable=True)
    contact_name = db.Column(db.String(64), nullable=True)
    contact_email = db.Column(db.String(64), nullable=True)
    contact_phone = db.Column(db.String(64), nullable=True)

    sheets = db.relationship("Sheet", viewonly=True)

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(func.lower(cls.email) == func.lower(email)).first()
        if (
            user is not None
            and user.activated
            and check_password_hash(user.password, password)
        ):
            return user

    def reset_password(self):
        self.password_hash = ""
        self.reset_password_uid = gen_password_reset_id()
        self.save()

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self):
        return f"<User: {self.username}>"


class AnonymousUser(AnonymousUserMixin):
    pass
