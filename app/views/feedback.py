from flask import Blueprint, render_template, flash
from flask_mail import Message

from app.forms import FeedbackForm
from config import BaseConfig as conf
from app import mail

blueprint = Blueprint("feedback", __name__, url_prefix="/feedback")


@blueprint.route("/", methods=["GET", "POST"])
def feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        msg = Message(
            subject="New feedback",
            sender=conf.MAIL_DEFAULT_SENDER,
            recipients=[conf.MAIL_FEEDBACK_RECEIVER],
        )

        msg.html = render_template(
            "email/feedback.html",
            feedback_name=form.feedback_name.data,
            feedback_email=form.feedback_email.data,
            feedback_message=form.feedback_message.data,
            config=conf,
        )
        mail.send(msg)

        flash("Feedback sent", "success")
    elif form.is_submitted():
        flash("Invalid data", "danger")

    return render_template("user/feedback.html", form=form)
