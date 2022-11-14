from uuid import uuid4
from datetime import datetime

from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app.models import User, PasswordRecovery
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


@auth_blueprint.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        log(log.INFO, "User [%s] in logged in", current_user)
        return redirect(url_for("main.index"))

    form = ForgotPassword()
    if form.validate_on_submit():
        email = form.email.data

        # edit previous recovery request
        user = User.query.filter(User.email == email).first()
        if not user.password_recovery:
            user.password_recovery = PasswordRecovery(created_by=user)

        recovery_code = str(uuid4())
        user.password_recovery.recovery_code = recovery_code

        log(log.INFO, "Create recovery request [%s]", user)
        user.save()

        url = f'http://{conf.DOMAIN}{url_for("auth.password_recovery", recovery_code=recovery_code)}'

        # mail_controller = MailController()
        # mail_controller.send_password_recovery_mail(email, url)

        flash("We sent a password reset URL to your email", "success")

    return render_template("auth/forgot_password.html", form=form)


@auth_blueprint.route("/password_recovery/<recovery_code>", methods=["GET", "POST"])
def password_recovery(recovery_code):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    message = error = None
    recovery_request = PasswordRecovery.query.filter(
        PasswordRecovery.recovery_code == recovery_code
    ).first()
    if not recovery_request:
        log(log.INFO, "Password recovery request does not exists [%s]", recovery_code)
        error = "Password recovery request does not exists"
        return render_template(
            "etc/message_page.html",
            error=error,
        )
    elif recovery_request:
        period = recovery_request.created_at - datetime.now()
        period = period.total_seconds() / 60 * -1  # in minutes

        if period > 20:
            log(
                log.INFO,
                "Password recovery link is expired [%s]",
                recovery_request.user,
            )

            error = "Password recovery link is expired"
            return render_template(
                "etc/message_page.html",
                error=error,
            )

    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not recovery_request:
            log(
                log.INFO,
                "Password recovery request does not exists [%s]",
                recovery_code,
            )
            error = "Password recovery request does not exists"
            return render_template(
                "etc/message_page.html",
                error=error,
            )
        log(log.INFO, "Change password [%s]", recovery_request.user)
        user = recovery_request.user
        user.password = form.password.data
        user.save()
        recovery_request.delete()
        flash("Password has been changed.", "success")
        return redirect(url_for("auth.login"))

    return render_template(
        "auth/reset_password.html",
        form=form,
        recovery_code=recovery_code,
        message=message,
        error=error,
    )


@auth_blueprint.route("/confirm_email/<confirmation_token>", methods=["GET", "POST"])
def confirm_email(confirmation_token):
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    user = User.query.filter(User.confirmation_token == confirmation_token).first()
    if not user:
        log(
            log.INFO,
            "User with email confirmation token [%s] does not exists ",
            confirmation_token,
        )
        error = "User not found"
        return render_template(
            "etc/message_page.html",
            error=error,
        )

    log(
        log.INFO,
        "Confirm user [%s] email",
        user,
    )
    user.activated = True
    user.confirmation_token = None
    user.save()

    flash("Email confirmed.", "success")
    return redirect(url_for("auth.login"))
