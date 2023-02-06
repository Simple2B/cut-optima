from werkzeug.datastructures import FileStorage

import app.models as m


def test_settings(client, authorize):
    user: m.User = m.User.query.first()

    assert user

    # assert defaul values
    assert user.metric_system == m.User.MetricSystem.centimeter
    assert user.print_price == 0
    assert user.currency == m.User.Currency.dollar
    assert not user.is_price_per_sheet
    assert user.moq == 1
    assert user.cut_spacing == 0.5
    assert not user.is_enabled_buy_btn
    assert not user.buy_url
    assert not user.shop_name
    assert not user.contact_name
    assert not user.contact_email
    assert not user.contact_phone

    new_metric_system = m.User.MetricSystem.inch.value
    new_print_price = 100
    new_currency = m.User.Currency.euro.value
    new_moq = 100
    new_cut_spacing = 100
    new_is_enabled_buy_btn = True
    new_buy_url = "https://google.com/"
    new_name = "Bob"
    new_email = "dummy@email.com"
    new_phone = "+380966666666"

    logo_img = FileStorage(
        stream=open("tests/testing_data/1.jpeg", "rb"),
        filename="1.jpeg",
        content_type="img/jpeg",
    )

    client.post(
        "/settings",
        data={
            "metric_system": new_metric_system,
            "print_price": new_print_price,
            "currency": new_currency,
            "is_price_per": "Sheet",
            "moq": new_moq,
            "cut_spacing": new_cut_spacing,
            "is_enabled_buy_btn": new_is_enabled_buy_btn,
            "buy_url": new_buy_url,
            "logo_img": logo_img,
            "contact_name": new_name,
            "contact_email": new_email,
            "contact_phone": new_phone,
        },
        follow_redirects=True,
    )

    assert user.metric_system == m.User.MetricSystem[new_metric_system]
    assert user.print_price == new_print_price
    assert user.currency == m.User.Currency[new_currency]
    assert user.is_price_per_sheet
    assert user.moq == new_moq
    assert user.cut_spacing == new_cut_spacing
    assert user.is_enabled_buy_btn
    assert user.buy_url
    assert not user.shop_name
    assert user.logo_img
    assert user.contact_name == new_name
    assert user.contact_email == new_email
    assert user.contact_phone == new_phone

    response = client.post(
        "/settings",
        json={
            "metric_system": new_metric_system,
            "currency": new_currency,
            "is_price_per": "Sheet",
            "shop_name": "123",
            "contact_email": "saintkos.com",
            "contact_phone": "111111",
        },
        follow_redirects=True,
    )
    assert b"Printshop name cannot be number" in response.data
    assert b"Wrong email format" in response.data
    assert not user.shop_name

    new_shop_name = "shop-test"
    response = client.post(
        "/settings",
        json={
            "metric_system": new_metric_system,
            "currency": new_currency,
            "is_price_per": "Sheet",
            "shop_name": new_shop_name,
        },
        follow_redirects=True,
    )
    assert user.shop_name
    assert user.shop_name == new_shop_name


def test_sheet_create_delete(client, authorize):
    assert not m.Sheet.query.all()

    response = client.post(
        "/settings/sheet/create",
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "Width and height are required"
    assert not m.Sheet.query.all()

    # incorrect size
    response = client.post(
        "/settings/sheet/create",
        json=dict(width=0, height=100),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "Size value cannot be 0 or less"
    assert not m.Sheet.query.all()

    response = client.post(
        "/settings/sheet/create",
        json=dict(width=-1, height=-1.5),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "Size value cannot be 0 or less"
    assert not m.Sheet.query.all()

    # integer sizes
    response = client.post(
        "/settings/sheet/create",
        json=dict(width=100, height=100),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "success"
    assert len(m.Sheet.query.all()) == 1

    # float sizes
    response = client.post(
        "/settings/sheet/create",
        json=dict(width=50.5, height=50.5),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "success"
    assert len(m.Sheet.query.all()) == 2

    sheet = m.Sheet.query.first()
    new_width = 10.0
    new_height = 10.0

    assert sheet.width != new_width
    assert sheet.height != new_height

    # price
    price = 10
    response = client.post(
        "/settings/sheet/create",
        json=dict(width=50.5, height=50.5, price=price),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "success"
    assert res["id"]

    sheet = m.Sheet.query.get(res["id"])
    assert sheet.price == price

    # moq
    moq = 10
    response = client.post(
        "/settings/sheet/create",
        json=dict(width=50.5, height=50.5, moq=moq),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "success"
    assert res["id"]

    sheet = m.Sheet.query.get(res["id"])
    assert sheet.moq == moq

    # use_in_row = true
    use_in_row = True
    response = client.post(
        "/settings/sheet/create",
        json=dict(width=50.5, height=50.5, use_in_row=use_in_row),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "success"
    assert res["id"]

    sheet = m.Sheet.query.get(res["id"])
    assert sheet.use_in_row == use_in_row

    # use_in_row = false
    use_in_row = False
    response = client.post(
        "/settings/sheet/create",
        json=dict(width=50.5, height=50.5, use_in_row=use_in_row),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "success"
    assert res["id"]

    sheet = m.Sheet.query.get(res["id"])
    assert sheet.use_in_row == use_in_row

    sheet_to_delete = m.Sheet.query.first()
    assert sheet_to_delete

    response = client.delete(
        "/settings/sheet/delete",
        json=dict(id=sheet_to_delete.id),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "success"
    deleted_sheet = m.Sheet.query.get(sheet_to_delete.id)
    assert not deleted_sheet

    response = client.delete(
        "/settings/sheet/delete",
        json=dict(id=100),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "Sheet not found"

    response = client.delete(
        "/settings/sheet/delete",
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "id is required"
