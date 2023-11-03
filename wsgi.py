#!/user/bin/env python
from app import create_app, db, models, forms

app = create_app()


# flask cli context setup
@app.shell_context_processor
def get_context():
    """Objects exposed here will be automatically available from the shell."""
    return dict(app=app, db=db, m=models, f=forms)


@app.cli.command()
def example_command():
    """Create the configured database."""
    print("Hello World!!!")


@app.cli.command()
def create_anonymous_user():
    """Create anonymous user."""
    user = models.User(
        username="anonymous_user_one_calc",
        email="anonymous_user_one_calc@anonymous_user_one_calc.com",
    )
    user.save()
    print("Anonymous user created.")


if __name__ == "__main__":
    app.run()
