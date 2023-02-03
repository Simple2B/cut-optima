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
        current_user.currency = form.currency.data
        current_user.is_price_per_sheet = form.is_price_per.data == "Sheet"
        current_user.moq = form.moq.data
        current_user.cut_spacing = form.cut_spacing.data
        current_user.is_enabled_buy_btn = form.is_enabled_buy_btn.data
        current_user.buy_url = form.buy_url.data
        current_user.shop_name = form.shop_name.data
        current_user.logo_img = form.logo_img.data
        current_user.logo_file_name = form.logo_file_name.data

        current_user.save()
        flash("Updated", "success")
    elif form.is_submitted():
        flash("Invalid data", "danger")

    return render_template("user/settings.html", form=form)


@blueprint.route("/sheet/create", methods=["POST"])
@login_required
def sheet_create():
    data = request.json if request.json else {}

    width = float(data.get("width")) if data.get("width") is not None else None
    height = float(data.get("height")) if data.get("height") is not None else None
    price = float(data.get("price")) if data.get("price") is not None else 0
    moq = int(data.get("moq")) if data.get("moq") not in ["", None] else 1
    use_in_row = (
        bool(data.get("use_in_row")) if data.get("use_in_row") is not None else False
    )

    if width is None or height is None:
        return jsonify({"message": "Width and height are required"}), 400
    elif width <= 0 or height <= 0:
        return jsonify({"message": "Size value cannot be 0 or less"}), 400

    sheet = m.Sheet(
        user=current_user,
        width=width,
        height=height,
        price=price,
        moq=moq,
        use_in_row=use_in_row,
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
