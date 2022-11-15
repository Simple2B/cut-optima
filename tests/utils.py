def register(client, username, email):
    return client.post(
        "/register",
        data=dict(
            username=username,
            email=email,
        ),
        follow_redirects=True,
    )


def login(client, email, password):
    return client.post(
        "/login", data=dict(email=email, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)
