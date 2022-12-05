from flask_login import UserMixin, AnonymousUserMixin

from app import db
from app.models.utils import ModelMixin


class Sheet(db.Model, UserMixin, ModelMixin):
    __tablename__ = "sheets"

    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    width = db.Column(db.Float(), default=0)
    height = db.Column(db.Float(), default=0)
    price = db.Column(db.Float(), default=0)
    moq = db.Column(db.Integer(), default=0)

    user = db.relationship("User")

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self):
        return f"<Sheet: {self.width}x{self.height}>"


class AnonymousUser(AnonymousUserMixin):
    pass
