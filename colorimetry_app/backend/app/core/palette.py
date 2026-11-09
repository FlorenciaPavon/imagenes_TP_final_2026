import colorsys
from PIL import Image
import math


def rgb_to_hsv(rgb: tuple[int, int, int]) -> tuple[float, float, float]:   
    """
    Convierte un color RGB (0-255) a HSV (0-1).
    """

    normalized = tuple(channel / 255 for channel in rgb)

    hsv = colorsys.rgb_to_hsv(*normalized)

    return hsv


def rgb_to_lab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:#usamos CIELAB

    new_lab = []

    pixel = Image.new("RGB", (1, 1), rgb)
    lab = pixel.convert("LAB").getpixel((0, 0))

    l = lab[0] * 100 / 255
    new_lab.append(l)

    a = lab[1] - 128
    new_lab.append(a)

    b = lab[2] - 128
    new_lab.append(b)

    return tuple(new_lab)

def get_lab_chromaticity(a: float, b: float) -> tuple[float, float]:

    list_crhom =[]

    #chromaticity
    c = math.sqrt(a**2 + b**2)
    list_crhom.append(c)

    # Degrees
    h =math.degrees(math.atan2(a,b))  % 360
    list_crhom.append(h)

    return tuple(list_crhom)


def describe_color(rgb: tuple[int, int, int]) -> dict:
    hsv= rgb_to_hsv(rgb)
    lab=rgb_to_lab(rgb)

    l,a,b=rgb_to_lab(rgb)
    c,h=get_lab_chromaticity(a,b)

    description = {
        "rgb": rgb,
        "hsv": hsv,
        "lab": lab,
        "chromaticity": c,
        "hue_angle": h
    }

    return description


def contrast(skin_v, eyes_v, hair_v):
    
    v_max= max(skin_v, eyes_v, hair_v)
    v_min= min(skin_v, eyes_v, hair_v)

    contrast = v_max-v_min

    return contrast

def classify_contrast():
    pass

def get_luminosity_contrast(skin_l: float, eyes_l: float, hair_l: float) -> float:
    l_max= max(skin_l, eyes_l, hair_l)
    l_min= min(skin_l, eyes_l, hair_l)

    contrast = l_max-l_min

    return contrast

def analyze_color_relationships(skin_rgb: tuple[int, int, int], eyes_rgb: tuple[int, int, int], hair_rgb: tuple[int, int, int]) -> dict:

    skin = describe_color(skin_rgb)
    eyes = describe_color(eyes_rgb)
    hair = describe_color(hair_rgb)

    skin_l = skin["lab"][0]
    skin_v = skin["hsv"][2]

    eyes_l = eyes["lab"][0]
    eyes_v = eyes["hsv"][2]

    hair_l = hair["lab"][0]
    hair_v = hair["hsv"][2]

    hsv_contrast = contrast(skin_v,eyes_v,hair_v)
    lum_contratst= get_luminosity_contrast(skin_l,eyes_l,hair_l)

    colors_relationships= {
        "skin": skin,
        "eyes": eyes,
        "hair":hair,
        "luminosity_contrast": {
            "hsv": hsv_contrast,
            "lab": lum_contratst
        }
    }

    return colors_relationships
