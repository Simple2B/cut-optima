from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user


from app.forms import FeedbackForm

blueprint = Blueprint("privacy", __name__, url_prefix="/privacy")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def privacy():
    form = FeedbackForm()

    if form.validate_on_submit():
        current_user.feedback_name = form.feedback_name.data
        current_user.feedback_email = form.feedback_email.data
        current_user.feedback_message = form.feedback_message.data

        current_user.save()
        flash("Updated", "success")
    elif form.is_submitted():
        flash("Invalid data", "danger")

    return render_template("user/privacy.html", form=form)
