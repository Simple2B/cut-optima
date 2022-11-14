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
