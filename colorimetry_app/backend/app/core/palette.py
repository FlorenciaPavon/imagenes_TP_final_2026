import colorsys


def rgb_to_hsv(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    """
    Convierte un color RGB (0-255) a HSV (0-1).
    """

    normalized = tuple(channel / 255 for channel in rgb)

    hsv = colorsys.rgb_to_hsv(*normalized)

    return hsv

def contrast(skin_v, eyes_v, hair_v):
    
    v_max= max(skin_v, eyes_v, hair_v)
    v_min= min(skin_v, eyes_v, hair_v)

    contrast = v_max-v_min

    return contrast

def classify_contrast():
    pass