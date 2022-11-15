import pytest

from app.controllers import RectPacker


@pytest.fixture
def rect_packer():
    yield RectPacker()


def test_basic_rect_packer_functionality(rect_packer: RectPacker):
    # validate without bins
    with pytest.raises(ValueError):
        rect_packer.validate_rectangles()

    BIN = [1000, 1000]
    assert not rect_packer.bins
    rect_packer.add_bin(*BIN)
    assert BIN in rect_packer.bins

    # validate without rectangles
    with pytest.raises(ValueError):
        rect_packer.validate_rectangles()

    RECT = [100, 100]
    assert not rect_packer.rectangles
    rect_packer.add_rectangle(*RECT)
    assert RECT in rect_packer.rectangles

    # validate with valid rectangle
    rect_packer.validate_rectangles()

    # validate with invalid rectangle
    INVALID_RECT = [1001, 100]
    rect_packer.add_rectangle(*INVALID_RECT)

    with pytest.raises(ValueError):
        rect_packer.validate_rectangles()

    # validate with larger bin
    rect_packer.add_bin(1500, 1500)
    rect_packer.validate_rectangles()

    # validate with blade size
    rect_packer.blade_size = 400
    with pytest.raises(ValueError):
        rect_packer.validate_rectangles()

    rect_packer.blade_size = 100
    rect_packer.validate_rectangles()

    rect_packer.pack()

    result = rect_packer.result

    for bin in result["bins"]:
        assert "image" in bin
        assert bin["image"]
        assert "sizes" in bin
        assert bin["sizes"] in rect_packer.bins
        assert "rectangles" in bin
        for rect in bin["rectangles"]:
            assert sorted(rect) in rect_packer.rectangles

        bin_area = bin["sizes"][0] * bin["sizes"][1]
        assert bin_area
        assert "used_area" in bin
        assert bin["used_area"] <= bin_area
        assert "wasted_area" in bin
        assert bin["wasted_area"] <= bin_area

    assert "not_placed_rectangles" in result
    assert len(result["not_placed_rectangles"]) <= len(rect_packer.rectangles)


def test_with_summary_rects_area_larger_than_bin_area(rect_packer: RectPacker):
    BIN = [1000, 1000]
    BIN_AREA = BIN[0] * BIN[1]
    RECTS_AREA = 0
    rect_packer.add_bin(*BIN)

    while RECTS_AREA <= BIN_AREA:
        RECT = [150, 210]
        RECTS_AREA += RECT[0] * RECT[1]
        rect_packer.add_rectangle(*RECT)

    rect_packer.validate_rectangles()

    rect_packer.pack()

    result = rect_packer.result

    for bin in result["bins"]:
        assert "image" in bin
        assert bin["image"]
        assert "sizes" in bin
        assert bin["sizes"] in rect_packer.bins
        assert "rectangles" in bin
        for rect in bin["rectangles"]:
            assert sorted(rect) in rect_packer.rectangles

        bin_area = bin["sizes"][0] * bin["sizes"][1]
        assert bin_area
        assert "used_area" in bin
        assert bin["used_area"] <= bin_area
        assert "wasted_area" in bin
        assert bin["wasted_area"] <= bin_area

    assert "not_placed_rectangles" in result
    assert len(result["not_placed_rectangles"]) <= len(rect_packer.rectangles)
