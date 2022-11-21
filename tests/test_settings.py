from app.models import Sheet, User


def test_settings(client, authorize):
    user = User.query.first()

    assert user

    # assert defaul values
    assert user.metric_system == User.MetricSystem.centimeter
    assert user.print_price == 0
    assert not user.is_price_per_sheet
    assert user.moq == 1
    assert user.cut_spacing == 0.5
    assert not user.is_enabled_buy_btn
    assert not user.buy_url

    new_metric_system = User.MetricSystem.inch.value
    new_print_price = 100
    new_moq = 100
    new_cut_spacing = 100
    new_is_enabled_buy_btn = True
    new_buy_url = "https://google.com/"

    client.post(
        "/settings",
        json={
            "metric_system": new_metric_system,
            "print_price": new_print_price,
            "is_price_per": "Sheet",
            "moq": new_moq,
            "cut_spacing": new_cut_spacing,
            "is_enabled_buy_btn": new_is_enabled_buy_btn,
            "buy_url": new_buy_url,
        },
        follow_redirects=True,
    )

    assert user.metric_system == new_metric_system
    assert user.print_price == new_print_price
    assert user.is_price_per_sheet
    assert user.moq == new_moq
    assert user.cut_spacing == new_cut_spacing
    assert user.is_enabled_buy_btn
    assert user.buy_url


def test_sheet_crud(client, authorize):
    assert not Sheet.query.all()

    response = client.post(
        "/settings/sheet/create",
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "Width and height are required"
    assert not Sheet.query.all()

    # incorect size
    response = client.post(
        "/settings/sheet/create",
        json=dict(width=0, height=100),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "Size value cannot be 0 or less"
    assert not Sheet.query.all()

    response = client.post(
        "/settings/sheet/create",
        json=dict(width=-1, height=-1.5),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "Size value cannot be 0 or less"
    assert not Sheet.query.all()

    # integer sizes
    response = client.post(
        "/settings/sheet/create",
        json=dict(width=100, height=100),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "success"
    assert len(Sheet.query.all()) == 1

    # float sizes
    response = client.post(
        "/settings/sheet/create",
        json=dict(width=50.5, height=50.5),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "success"
    assert len(Sheet.query.all()) == 2

    sheet_to_update = Sheet.query.first()
    new_width = 10.0
    new_height = 10.0

    assert sheet_to_update.width != new_width
    assert sheet_to_update.height != new_height

    response = client.patch(
        "/settings/sheet/update",
        json=dict(id=100, width=50.5, height=50.5),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "Sheet not found"

    response = client.patch(
        "/settings/sheet/update",
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "id, width and height are required"

    sheet_to_delete = Sheet.query.first()
    assert sheet_to_delete

    response = client.delete(
        "/settings/sheet/delete",
        json=dict(id=sheet_to_update.id),
        follow_redirects=True,
    )
    res = response.json
    assert res
    assert res["message"] == "success"
    deleted_sheet = Sheet.query.get(sheet_to_update.id)
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
