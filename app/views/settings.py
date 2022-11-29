from flask import jsonify, Blueprint, request, render_template, flash
from flask_login import login_required, current_user

from app.models import Sheet, User
from app.forms import SettingsForm, AddSheet

blueprint = Blueprint("settings", __name__, url_prefix="/settings")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def settings():
    form = SettingsForm()

    if form.validate_on_submit():
        current_user.metric_system = User.MetricSystem[form.metric_system.data]
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
    form = AddSheet()

    if form.validate_on_submit():
        sheet = Sheet(
            user=current_user,
            width=form.width.data,
            height=form.height.data,
        )
        sheet.save()
    elif form.is_submitted():
        if form.width.data is None or form.height.data is None:
            return jsonify({"message": "Width and height are required"}), 400
        elif form.width.data <= 0 or form.height.data <= 0:
            return jsonify({"message": "Size value cannot be 0 or less"}), 400

    return jsonify({"message": "success"})


@blueprint.route("/sheet/update", methods=["PATCH"])
@login_required
def sheet_update():
    data = request.json if request.json else {}

    sheet_id = data.get("id")
    width = data.get("width")
    height = data.get("height")

    if sheet_id is None or width is None or height is None:
        return jsonify({"message": "id, width and height are required"}), 400
    elif width <= 0 or height <= 0:
        return jsonify({"message": "Size value cannot be 0 or less"}), 400

    sheet = Sheet.query.get(sheet_id)
    if not sheet or sheet.user != current_user:
        return jsonify({"message": "Sheet not found"}), 400

    sheet.width = width
    sheet.height = height
    sheet.save()

    return jsonify({"message": "success"})


@blueprint.route("/sheet/delete", methods=["DELETE"])
@login_required
def sheet_delete():
    data = request.json if request.json else {}

    sheet_id = data.get("id")
    if sheet_id is None:
        return jsonify({"message": "id is required"}), 400

    sheet = Sheet.query.get(sheet_id)
    if not sheet or sheet.user != current_user:
        return jsonify({"message": "Sheet not found"}), 400

    sheet.delete()

    return jsonify({"message": "success"})
