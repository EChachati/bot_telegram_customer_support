import cv2
from pyzbar.pyzbar import decode


def get_barcode(path) -> str:
    _code = 'NO LEGIBLE'
    img = decode(cv2.imread(path))
    for obj in img:
        _code = f'{obj.data}'
    return _code.replace("b", "").replace("'", "")
