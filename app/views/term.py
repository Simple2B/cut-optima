from flask import Blueprint, render_template

blueprint = Blueprint("term", __name__, url_prefix="/term")


@blueprint.route("/", methods=["GET", "POST"])
def term():
    return render_template("term.html")
