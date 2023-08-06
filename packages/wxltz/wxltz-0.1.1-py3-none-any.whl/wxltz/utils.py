from wxltz.models import HSV, Proportion
from typing import Literal
import colorsys
import pywal


def hex_to_hsv(hex_str: str) -> HSV:
    rgb = map(lambda x: Proportion(x / 255), pywal.colors.util.hex_to_rgb(hex_str))
    return HSV(*colorsys.rgb_to_hsv(*rgb))


def hsv_to_hex(hsv: HSV) -> str:
    rgb = tuple(map(lambda x: int(x * 255), colorsys.hsv_to_rgb(*hsv)))
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def shade(hsv: HSV, scale: Proportion, how: Literal["tint", "shade"] = "shade") -> HSV:
    if how == "shade":
        vib = Proportion(hsv.vib * (1 - scale))
    else:
        vib = Proportion(hsv.vib * (1 + scale))
    return HSV(hsv.hue, hsv.sat, vib)
