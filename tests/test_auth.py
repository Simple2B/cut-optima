from typing import List
from tests.utils import register, login, logout
from app.models import User

from .constants import EMAIL, PASSWORD, USERNAME


def test_auth_pages(client):
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200
    response = client.get("/logout")
    assert response.status_code == 302
    response = client.get("/reset_password")
    assert response.status_code == 200


def test_register(client):
    # register with invalid passwords
    response = client.post(
        "/register",
        data=dict(username=USERNAME, email="EMAIL"),
        follow_redirects=True,
    )
    assert b"The given data was invalid." in response.data

    # register with valid data
    response = client.post(
        "/register",
        data=dict(
            username=USERNAME,
            email=EMAIL,
        ),
        follow_redirects=True,
    )
    assert b"Please visit your email address to set you password" in response.data

    user: User = User.query.filter(User.email == EMAIL).first()
    assert user
    assert user.email == EMAIL
    assert user.username == USERNAME
    assert user.reset_password_uid
    assert not user.activated

    # register with used email
    response = client.post(
        "/register",
        data=dict(username=USERNAME, email=EMAIL),
        follow_redirects=True,
    )
    assert b"The given data was invalid." in response.data
    assert b"This email is already registered." in response.data

    users: List[User] = User.query.filter(User.email == EMAIL).all()
    assert users
    assert len(users) == 1


def test_login_email_confirming_logout(client):
    # Access to logout view before login should fail.
    response = logout(client)
    assert b"Please log in to access this page." in response.data

    response = register(client, USERNAME, EMAIL)
    assert b"Please visit your email address to set you password" in response.data

    # login not activated user
    response = login(client, EMAIL, PASSWORD)
    assert b"Wrong email or password" in response.data

    # activation user
    user: User = User.query.filter(User.email == EMAIL).first()
    response = client.post(
        "/password_recovery/" + user.reset_password_uid,
        data=dict(
            password=PASSWORD,
            confirm_password=PASSWORD,
        ),
        follow_redirects=True,
    )
    assert b"Login successful." in response.data

    # Should successfully logout the currently logged in user.
    response = logout(client)
    assert b"You were logged out." in response.data

    # login activated user
    response = login(client, EMAIL, PASSWORD)
    assert b"Login successful." in response.data

    response = login(client, EMAIL, PASSWORD)
    assert b"You are already logged in." in response.data

    # Should successfully logout the currently logged in user.
    response = logout(client)
    assert b"You were logged out." in response.data

    # # Incorrect login credentials should fail.
    response = login(client, EMAIL, "wrongpassword")
    assert b"Wrong email or password." in response.data


def test_password_recovery(client):
    response = client.post(
        "/reset_password",
        data=dict(
            email=EMAIL,
        ),
        follow_redirects=True,
    )
    assert b"Email not found" in response.data
    assert b"No registered user with this e-mail" in response.data

    response = register(client, USERNAME, EMAIL)
    assert b"Please visit your email address to set you password" in response.data

    response = client.post(
        "/reset_password",
        data=dict(
            email=EMAIL,
        ),
        follow_redirects=True,
    )
    assert (
        b"Password reset successful. For set new password please check your e-mail."
        in response.data
    )

    user: User = User.query.filter(User.email == EMAIL).first()
    assert user.reset_password_uid

    new_password = "new_password"
    # passwords do not match
    response = client.post(
        "/password_recovery/" + user.reset_password_uid,
        data=dict(
            password=new_password,
            confirm_password=new_password + "123",
        ),
        follow_redirects=True,
    )
    assert b"Passwords must match" in response.data

    # passwords match
    response = client.post(
        "/password_recovery/" + user.reset_password_uid,
        data=dict(
            password=new_password,
            confirm_password=new_password,
        ),
        follow_redirects=True,
    )
    assert b"Login successful." in response.data
