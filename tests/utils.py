import app.models as m


def register(client, username, email):
    return client.post(
        "/register",
        data=dict(
            username=username,
            email=email,
        ),
        follow_redirects=True,
    )


def activate_user(username, password):
    user: m.User = m.User.query.filter(m.User.username == username).first()
    user.password = password
    user.activated = True
    user.save()


def login(client, email, password):
    return client.post(
        "/login", data=dict(email=email, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)
