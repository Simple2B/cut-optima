from flask import Blueprint, render_template, request, jsonify
from rectpack import (
    skyline,
    guillotine,
    SORT_PERI,
    SORT_SSIDE,
    SORT_DIFF,
    SORT_RATIO,
    SORT_AREA,
    SORT_LSIDE,
    SORT_NONE,
)

from config import BaseConfig as conf
from app.controllers import RectPacker
from app.models import User
from app.utils import serve_pil_image
from app.logger import log

blueprint = Blueprint("calculator", __name__)


@blueprint.route("/calculator/<printshop>", methods=["GET"])
@blueprint.route("/calculator", methods=["GET"])
def calculator(printshop: str = None):
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
    show_settings = True
    img = None
    contact_name = None
    contact_email = None
    contact_phone = None

    if not printshop:
        printshop = request.args.get("printshop")
    if printshop:
        user = User.query.filter(User.shop_name == printshop).first()
        if not user and printshop.isnumeric():
            user = User.query.get(printshop)

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
            show_settings = False
            img = user.logo_img
            contact_name = user.contact_name
            contact_email = user.contact_email
            contact_phone = user.contact_phone

    return render_template(
        "calculator/index.html",
        config=conf,
        show_settings=show_settings,
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
        img=img,
        contact_name=contact_name,
        contact_email=contact_email,
        contact_phone=contact_phone,
    )


@blueprint.route("/calculate", methods=["POST"])
def calculate():
    data = request.json

    log(log.INFO, "Validate required data [%s]", data)

    if not data.get("bins"):
        return jsonify({"message": "Bin(s) not found"}), 400
    elif not data.get("rectangles"):
        return jsonify({"message": "Rectangle(s) not found"}), 400
    elif data.get("meticSystem") not in ["cm", "in"]:
        return jsonify({"message": "Invalid metic system"}), 400

    log(log.INFO, "Calculate and validate square_unit")
    metic_system = data.get("meticSystem")
    square_unit = conf.METRIC_TO_SQR_UNIT_VALUE.get(metic_system)
    if not square_unit:
        return jsonify({"message": "Incorrect metric system"}), 400

    print_price = data.get("printPrice") or 0
    moq = data.get("moqQty") or 0

    price_per = data.get("pricePer")
    blade_size = data["bladeSize"]

    first_bin = data["bins"][0]
    is_sizes_equals = first_bin["size"][0] == first_bin["size"][1]
    if is_sizes_equals:
        # to make width as larger side if sizes equals
        first_bin["size"][0] += 1

    log(log.INFO, "Init RectPacker")
    rect_packer = RectPacker(
        blade_size=blade_size / 2,
        is_sizes_equals=is_sizes_equals,
        square_unit=square_unit,
        price_per=price_per,
        print_price=print_price,
        moq=moq,
    )

    log(log.INFO, "Add bins to RectPacker instance")
    for bin in data["bins"]:
        for _ in range(bin["pics"]):
            width = bin["size"][0]
            height = bin["size"][1]
            rect_packer.add_bin(width, height)

    log(log.INFO, "Add rects to RectPacker instance")
    for rect in data["rectangles"]:
        for _ in range(rect["pics"]):
            width = rect["size"][0]
            height = rect["size"][1]
            rect_packer.add_rectangle(width, height)

    try:
        log(log.INFO, "Validate added data to RectPacker instance")
        rect_packer.validate_rectangles()
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    use_in_row = data.get("useInRow")

    results = {}
    log(log.INFO, "Start find the best packing algo")
    for pack_algo in [
        skyline.SkylineBl,
        skyline.SkylineBlWm,
        skyline.SkylineMwf,
        skyline.SkylineMwfl,
        skyline.SkylineMwfWm,
        skyline.SkylineMwflWm,
        guillotine.GuillotineBssfSas,
        guillotine.GuillotineBssfLas,
        guillotine.GuillotineBssfSlas,
        guillotine.GuillotineBssfLlas,
        guillotine.GuillotineBssfMaxas,
        guillotine.GuillotineBssfMinas,
        guillotine.GuillotineBlsfSas,
        guillotine.GuillotineBlsfLas,
        guillotine.GuillotineBlsfSlas,
        guillotine.GuillotineBlsfLlas,
        guillotine.GuillotineBlsfMaxas,
        guillotine.GuillotineBlsfMinas,
        guillotine.GuillotineBafSas,
        guillotine.GuillotineBafLas,
        guillotine.GuillotineBafSlas,
        guillotine.GuillotineBafLlas,
        guillotine.GuillotineBafMaxas,
        guillotine.GuillotineBafMinas,
    ]:
        for sort_algo in [
            SORT_NONE,
            SORT_RATIO,
            SORT_PERI,
            SORT_SSIDE,
            SORT_DIFF,
            SORT_AREA,
            SORT_LSIDE,
        ]:
            try:
                log(log.INFO, "Generate sesult using [%s] algo", pack_algo)
                rect_packer.reset(bins_in_row=1, reset_bin_sizes=True)
                rect_packer.pack(
                    use_sheet_in_row=use_in_row,
                    pack_algo=pack_algo,
                    sort_algo=sort_algo,
                )
                result = rect_packer.result
                if not result.get("placed_items"):
                    continue
                result["algo"] = str(pack_algo)

                used_area = result["used_area"]
                if not results.get(used_area):
                    results[used_area] = []
                results[used_area].append(result)
            except RecursionError:
                log(log.EXCEPTION, "RecursionError")

    log(log.INFO, "Find the best result")
    min_used_area = min(results.keys())

    best_results = results[min_used_area]
    best_results = sorted(
        best_results,
        key=lambda res: (res["wasted_area"], res["used_bins"]),
    )

    result = best_results[0]
    color_schema = {}
    log(log.INFO, "Generate images for results")
    for bin in result["bins"]:
        image = rect_packer.generate_image_for_bin(bin["bin"], color_schema)
        bin["image"] = serve_pil_image(image)
        del bin["bin"]
    del result["algo"]

    return jsonify(result)
