def register(client, username, email, password):
    return client.post(
        "/register",
        data=dict(
            username=username,
            email=email,
            password=password,
            password_confirmation=password,
        ),
        follow_redirects=True,
    )


def login(client, email, password):
    return client.post(
        "/login", data=dict(email=email, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)
