from flask import Blueprint, render_template

blueprint = Blueprint("privacy", __name__, url_prefix="/privacy")


@blueprint.route("/", methods=["GET", "POST"])
def privacy():
    return render_template("privacy.html")
