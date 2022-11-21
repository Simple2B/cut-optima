from flask import jsonify, Blueprint, request
from flask_login import login_required, current_user

from app.models import Sheet

blueprint = Blueprint("settings", __name__, url_prefix="/settings")


@blueprint.route("/sheet/create", methods=["POST"])
@login_required
def sheet_create():
    data = request.json if request.json else {}

    width = data.get("width")
    height = data.get("height")

    if width is None or height is None:
        return jsonify({"message": "Width and height are required"}), 400
    elif width <= 0 or height <= 0:
        return jsonify({"message": "Size value cannot be 0 or less"}), 400

    sheet = Sheet(
        user=current_user,
        width=width,
        height=height,
    )
    sheet.save()

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
    if not sheet:
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
    if not sheet:
        return jsonify({"message": "Sheet not found"}), 400

    sheet.delete()

    return jsonify({"message": "success"})
