from flask import Blueprint, render_template
from flask_login import login_user

from config import BaseConfig as conf

blueprint = Blueprint("calculator", __name__)


@login_required
@blueprint.route("/calculator", methods=["GET"])
def calculator():
    return render_template("calculator/index.html", config=conf)
