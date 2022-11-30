from flask import jsonify, Blueprint, render_template, flash, request
from flask_login import login_required, current_user

import app.models as m
from app.forms import SettingsForm

blueprint = Blueprint("settings", __name__, url_prefix="/settings")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def settings():
    form = SettingsForm()

    if form.validate_on_submit():
        current_user.metric_system = m.User.MetricSystem[form.metric_system.data]
        current_user.print_price = form.print_price.data
        current_user.is_price_per_sheet = form.is_price_per.data == "Sheet"
        current_user.moq = form.moq.data
        current_user.cut_spacing = form.cut_spacing.data
        current_user.is_enabled_buy_btn = form.is_enabled_buy_btn.data
        current_user.buy_url = form.buy_url.data

        current_user.save()
        flash("Updated", "success")

    return render_template("user/settings.html", form=form)


@blueprint.route("/sheet/create", methods=["POST"])
@login_required
def sheet_create():
    data = request.json if request.json else {}

    width = int(data.get("width")) if data.get("width") is not None else None
    height = int(data.get("height")) if data.get("height") is not None else None

    if width is None or height is None:
        return jsonify({"message": "Width and height are required"}), 400
    elif width <= 0 or height <= 0:
        return jsonify({"message": "Size value cannot be 0 or less"}), 400

    sheet = m.Sheet(
        user=current_user,
        width=width,
        height=height,
    )
    sheet.save()
    return jsonify({"message": "success", "id": sheet.id})


@blueprint.route("/sheet/delete", methods=["DELETE"])
@login_required
def sheet_delete():
    data = request.json if request.json else {}

    sheet_id = data.get("id")
    if sheet_id is None:
        return jsonify({"message": "id is required"}), 400

    sheet = m.Sheet.query.get(sheet_id)
    if not sheet or sheet.user != current_user:
        return jsonify({"message": "Sheet not found"}), 400

    sheet.delete()

    return jsonify({"message": "success"})
