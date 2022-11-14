from uuid import uuid4
from datetime import datetime

from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.models import User
from app.forms import LoginForm, RegistrationForm, ForgotPassword, ChangePasswordForm
from app.logger import log
from config import BaseConfig as conf

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        log(log.INFO, "Create user [%s]", user)
        user.save()

        # TODO SEND MAIL

        flash(
            "Please visit your email address to set you password",
            "success",
        )
        return redirect(url_for("main.index"))
    elif form.is_submitted():
        log(log.ERROR, "The given data was invalid")
        flash("The given data was invalid.", "danger")
    return render_template("auth/register.html", form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if not current_user.is_anonymous:
        log(log.INFO, "User [%s] is already logged in", current_user)
        flash("You are already logged in.", "danger")
        return redirect(url_for("main.index"))

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user: User = User.authenticate(form.email.data, form.password.data)
        if user:
            log(log.INFO, "Login user [%s]", user)
            login_user(user)
            flash("Login successful.", "success")
            return redirect(url_for("main.index"))
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


@auth_blueprint.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        log(log.INFO, "User [%s] in logged in", current_user)
        return redirect(url_for("main.index"))

    form = ForgotPassword()
    if form.validate_on_submit():
        email: str = form.email.data

        # edit previous recovery request
        user: User = User.query.filter(User.email == email.lower()).first()

        if user:
            log(log.INFO, "Create recovery request [%s]", user)
            user.reset_password()

            # TODO SEND MAIL

            flash(
                "Password reset successful. For set new password please check your e-mail.",
                "success",
            )
            return redirect(url_for("main.index"))
    flash("No registered user with this e-mail", "danger")
    return render_template("auth/forgot_password.html", form=form)


@auth_blueprint.route(
    "/password_recovery/<reset_password_uid>", methods=["GET", "POST"]
)
def password_recovery(reset_password_uid):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    message = error = None

    user: User = User.query.filter(
        User.reset_password_uid == reset_password_uid
    ).first()

    if not user:
        log(log.ERROR, "wrong reset_password_uid. [%s]", reset_password_uid)
        flash("Incorrect reset password link", "danger")
        return redirect(url_for("main.index"))

    form = ChangePasswordForm()

    if form.validate_on_submit():
        log(log.INFO, "Change password [%s]", user)
        user.password = form.password.data
        user.reset_password_uid = ""
        user.save()
        login_user(user)
        flash("Password has been changed.", "success")
        flash("Login successful.", "success")
        return redirect(url_for("main.index"))

    return render_template(
        "auth/reset_password.html",
        form=form,
        reset_password_uid=reset_password_uid,
        message=message,
        error=error,
    )
