from flask import Blueprint, render_template, request, jsonify

from config import BaseConfig as conf
from app.controllers import RectPacker
from app.utils import serve_pil_image
from app.models import User

blueprint = Blueprint("calculator", __name__)


@blueprint.route("/calculator", methods=["GET"])
def calculator():
    moq = ""
    moq_unit = ""
    cost = ""
    cost_per = ""
    order_url = ""
    order_enabled = False
    cut_spacing = 0.5
    metric_system = None
    sheets = None

    setup_id = request.args.get("setup_id")
    if setup_id:
        user: User = User.query.get(request.args.get("setup_id"))
        moq = user.moq
        moq_unit = "Sheet" if user.is_price_per_sheet else "SQR"
        cost = user.print_price
        cost_per = "Sheet" if user.is_price_per_sheet else "SQR"
        order_url = user.buy_url
        order_enabled = user.is_enabled_buy_btn
        cut_spacing = user.cut_spacing
        metric_system = user.metric_system.value
        sheets = user.sheets

    return render_template(
        "calculator/index.html",
        config=conf,
        setup_id=setup_id,
        moq=moq,
        moq_unit=moq_unit,
        cost=cost,
        cost_per=cost_per,
        order_url=order_url,
        order_enabled=order_enabled,
        cut_spacing=cut_spacing,
        metric_system=metric_system,
        sheets=sheets,
    )


@blueprint.route("/calculate", methods=["POST"])
def calculate():
    data = request.json

    if not data.get("bins"):
        return jsonify({"message": "Bin(s) not found"}), 400
    elif not data.get("rectangles"):
        return jsonify({"message": "Rectangle(s) not found"}), 400
    elif data.get("meticSystem") not in ["cm", "in"]:
        return jsonify({"message": "Invalid metic system"}), 400

    metic_system = data.get("meticSystem")
    rect_packer = RectPacker(blade_size=data["bladeSize"])

    for bin in data["bins"]:
        for _ in range(bin["pics"]):
            width = bin["size"][0]
            height = bin["size"][1]
            rect_packer.add_bin(width, height)

    for rect in data["rectangles"]:
        for _ in range(rect["pics"]):
            width = rect["size"][0]
            height = rect["size"][1]
            rect_packer.add_rectangle(width, height)

    try:
        rect_packer.validate_rectangles()
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    rect_packer.pack()

    print_sqr_price = 0
    if data.get("printPrice"):
        print_sqr_price = data.get("printPrice")

    square_unit = None
    if metic_system == "cm":
        # square meter
        square_unit = 100 * 100
    elif metic_system == "in":
        # square feet
        square_unit = 12 * 12

    res = {
        "used_area": 0,
        "wasted_area": 0,
        "placed_items": [],
        "print_price": 0,
        "bins": [],
    }
    for bin in rect_packer.result["bins"]:
        res["used_area"] += bin["used_area"] / square_unit
        res["wasted_area"] += bin["wasted_area"] / square_unit
        res["placed_items"] += bin["rectangles"]
        res["print_price"] += bin["used_area"] / square_unit * print_sqr_price

        res["bins"].append(
            {
                "sizes": bin["sizes"],
                "used_area": bin["used_area"],
                "wasted_area": bin["wasted_area"],
                "placed_items": bin["rectangles"],
                "print_price": bin["used_area"] / square_unit * print_sqr_price,
                "image": serve_pil_image(bin["image"]),
            }
        )

    return jsonify(res)
