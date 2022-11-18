from io import BytesIO
from base64 import encodebytes


def serve_pil_image(pil_img):
    byte_arr = BytesIO()
    pil_img.save(byte_arr, format="PNG")  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode("ascii")  # encode as base64
    return encoded_img
