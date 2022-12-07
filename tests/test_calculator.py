def test_calculate(client):
    # without bins
    INVALID_INPUT_DATA = {
        "bins": [],
        "rectangles": [
            {"size": [10, 10], "pics": 2},
            {"size": [15, 15], "pics": 5},
        ],
        "bladeSize": 10.5,
        "printPrice": 15.1,
        "meticSystem": "centimeter",
    }

    response = client.post(
        "/calculate",
        json=INVALID_INPUT_DATA,
        follow_redirects=True,
    )
    assert response.status_code == 400
    data = response.json
    assert data["message"] == "Bin(s) not found"

    # without rects
    INVALID_INPUT_DATA = {
        "bins": [{"size": [10, 10], "pics": 2}],
        "rectangles": [],
        "bladeSize": 10.5,
        "printPrice": 15.1,
        "meticSystem": "centimeter",
    }

    response = client.post(
        "/calculate",
        json=INVALID_INPUT_DATA,
        follow_redirects=True,
    )
    assert response.status_code == 400
    data = response.json
    assert data["message"] == "Rectangle(s) not found"

    # without rects
    INVALID_INPUT_DATA = {
        "bins": [{"size": [100, 100], "pics": 1}],
        "rectangles": [
            {"size": [10, 10], "pics": 2},
            {"size": [15, 15], "pics": 5},
        ],
        "bladeSize": 10.5,
        "printPrice": 15.1,
        "meticSystem": "ivalid",
    }

    response = client.post(
        "/calculate",
        json=INVALID_INPUT_DATA,
        follow_redirects=True,
    )
    assert response.status_code == 400
    data = response.json
    assert data["message"] == "Invalid metic system"

    INPUT_DATA = {
        "bins": [{"size": [100, 100], "pics": 1}],
        "rectangles": [
            {"size": [10, 10], "pics": 2},
            {"size": [15, 15], "pics": 5},
        ],
        "bladeSize": 2,
        "printPrice": 15.1,
        "meticSystem": "cm",
    }

    response = client.post(
        "/calculate",
        json=INPUT_DATA,
        follow_redirects=True,
    )
    assert response.status_code == 200
    data = response.json
    assert data["used_area"]
    assert data["wasted_area"]
    assert data["placed_items"]
    assert data["print_price"]
    assert data["bins"]
    for bin in data["bins"]:
        assert bin["used_area"]
        assert bin["wasted_area"]
        assert bin["placed_items"]
        assert bin["print_price"]
        assert bin["image"]
