from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user


from app.forms import FeedbackForm

blueprint = Blueprint("term", __name__, url_prefix="/term")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def term():
    form = FeedbackForm()

    if form.validate_on_submit():
        current_user.feedback_name = form.feedback_name.data
        current_user.feedback_email = form.feedback_email.data
        current_user.feedback_message = form.feedback_message.data

        current_user.save()
        flash("Updated", "success")
    elif form.is_submitted():
        flash("Invalid data", "danger")

    return render_template("user/term.html", form=form)
