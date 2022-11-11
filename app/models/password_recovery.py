from datetime import datetime

from app import db
from app.models.utils import ModelMixin


class PasswordRecovery(db.Model, ModelMixin):

    __tablename__ = "password_recovery"

    id = db.Column(db.Integer, primary_key=True)
    recovery_code = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<PasswordRecovery: {self.email}>"
