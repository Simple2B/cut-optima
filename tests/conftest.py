import pytest

from app import db, create_app
from tests.utils import register, login, activate_user
from .constants import EMAIL, PASSWORD, USERNAME


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        db.drop_all()
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()
        app_ctx.pop()


@pytest.fixture
def authorize(client):
    register(client, USERNAME, EMAIL)
    activate_user(USERNAME, PASSWORD)
    login(client, EMAIL, PASSWORD)
