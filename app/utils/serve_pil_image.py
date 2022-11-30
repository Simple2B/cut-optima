from io import BytesIO
from base64 import encodebytes

from PIL import Image

from app.logger import log


def serve_pil_image(pil_img: Image):
    byte_arr = BytesIO()
    log(log.INFO, "Save pil image as PNG")
    pil_img.save(byte_arr, format="PNG")  # convert the PIL image to byte array
    log(log.INFO, "Encode pil image as base64")
    encoded_img = encodebytes(byte_arr.getvalue()).decode("ascii")  # encode as base64
    return encoded_img
