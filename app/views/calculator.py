import math

from flask import Blueprint, render_template, request, jsonify

from config import BaseConfig as conf
from app.controllers import RectPacker
from app.utils import serve_pil_image
from app.models import User

blueprint = Blueprint("calculator", __name__)


@blueprint.route("/calculator", methods=["GET"])
def calculator():
    moq = conf.MOQ
    moq_unit = conf.MOQ_UNIT
    cost = conf.COST
    cost_per = conf.COST_PER
    order_url = conf.ORDER_URL
    order_enabled = conf.ORDER_ENABLED
    cut_spacing = conf.CUT_SPACING
    metric_system = conf.METRIC_SYSTEM
    sheets = conf.SHEETS
    currency = conf.CURRENCY

    setup_id = request.args.get("setup_id")
    if setup_id:
        user: User = User.query.get(request.args.get("setup_id"))
        if user:
            moq = user.moq
            moq_unit = "Sheet" if user.is_price_per_sheet else "SQR"
            cost = user.print_price
            cost_per = "Sheet" if user.is_price_per_sheet else "SQR"
            order_url = user.buy_url
            order_enabled = user.is_enabled_buy_btn
            cut_spacing = user.cut_spacing
            metric_system = user.metric_system.value
            sheets = user.sheets
            currency = conf.CURRENCY_NAME_TO_SYMBOL[user.currency.value]

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
        currency=currency,
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
    price_per = data.get("pricePer")

    first_bin = data["bins"][0]
    is_sizes_equals = first_bin["size"][0] == first_bin["size"][1]
    if is_sizes_equals:
        # to make width as larger side if sizes equals
        first_bin["size"][0] += 1
    rect_packer = RectPacker(
        blade_size=data["bladeSize"],
        is_bin_width_larger=first_bin["size"][0] > first_bin["size"][1],
        is_sizes_equals=is_sizes_equals,
    )

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

    use_in_row = data.get("useInRow")

    rect_packer.pack(use_sheet_in_row=use_in_row)

    print_price = 0
    if data.get("printPrice"):
        print_price = data.get("printPrice")

    moq = 0
    if data.get("moqQty"):
        moq = data.get("moqQty")

    moq_price = print_price * moq

    square_unit = conf.METRIC_TO_SQR_UNIT_VALUE.get(metic_system)
    if not square_unit:
        return jsonify({"message": "Incorrect metric system"}), 400

    used_bins_count = (
        rect_packer.result["used_bins"]
        if len(rect_packer.result["bins"]) == 1
        else len(rect_packer.result["bins"])
    )

    res = {
        "used_area": 0,
        "wasted_area": 0,
        "placed_items": [],
        "print_price": 0,
        "bins": [],
        "used_bins": used_bins_count,
    }
    for bin in rect_packer.result["bins"]:
        if is_sizes_equals:
            bin["sizes"][0] -= 1

        # wasted area calculated by max_y_coordinate * width
        reduced_height = bin["sizes"][1] - bin["max_y_coordinate"]
        if reduced_height <= 0:
            reduced_height = bin["sizes"][1]
        res["used_area"] += ((bin["sizes"][0] * bin["max_y_coordinate"])) / square_unit
        if res["used_area"] != 1:
            res["wasted_area"] += bin["sizes"][0] * reduced_height / square_unit
        else:
            res["wasted_area"] += 0
        res["placed_items"] += bin["rectangles"]

        if price_per == "sqr":
            res["print_price"] = res["used_area"] * print_price
        else:
            res["print_price"] += print_price

        res["bins"].append(
            {
                "sizes": bin["sizes"],
                "used_area": bin["used_area"],
                "wasted_area": bin["wasted_area"],
                "placed_items": bin["rectangles"],
                "print_price": (math.prod(bin["sizes"]) / square_unit) * print_price,
                "image": serve_pil_image(bin["image"]),
            }
        )

    if res["print_price"] < moq_price and moq > 0:
        res["print_price"] = moq_price

    return jsonify(res)
