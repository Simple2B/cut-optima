from uuid import uuid4

from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.logger import log

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            confirmation_token=str(uuid4()),
        )
        log(log.INFO, "Create user [%s]", user)
        user.save()
        flash("Please visit your email address to verify it", "success")
        return redirect(url_for("main.index"))
    elif form.is_submitted():
        log(log.ERROR, "The given data was invalid")
        flash("The given data was invalid.", "danger")
    return render_template("auth/register.html", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if not current_user.is_anonymous:
        log(log.INFO, "User [%s] is already logged in", current_user)
        flash("You are already logged in.")
        return redirect(url_for("main.index"))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user: User = User.authenticate(form.email.data, form.password.data)
        if user is not None and user.activated:
            log(log.INFO, "Login user [%s]", user)
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("main.index"))
        elif user and not user.activated:
            log(log.ERROR, "Cannot login in. User [%s] is not activated", user)
            flash("Cannot login in. Please confirm your email.", "danger")
        else:
            log(log.ERROR, "Wrong email or password")
            flash("Wrong email or password.", "danger")
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    log(log.INFO, "Logout user [%s]", current_user)
    logout_user()
    flash("You were logged out.", "info")
    return redirect(url_for("main.index"))
