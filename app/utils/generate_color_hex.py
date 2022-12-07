# flake8: noqa F731
import random


def generate_color_hex():
    """Generage not bright color hex

    Returns:
        str: color hex
    """
    r = lambda min_value=0, max_value=150: random.randint(0, max_value)
    return "#%02X%02X%02X" % (r(100, 200), r(100, 200), r(100, 200))
