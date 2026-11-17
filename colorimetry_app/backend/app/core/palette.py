import colorsys
from PIL import Image
import math

'''
El calculo de umbrales de claridad y croma se hizo teniendo en cuenta el archivo Skin Database 1-92-xlsx obtenido desde https://cie.co.at/technicalcommittees/skin-colour-database
corresponde al origen 1 (UK) y las ubicaciones 2 (mejilla), 3 (pómulo), 4 (mentón) y 6 (frente): 150 sujetos, una medición por sujeto en cada zona, 600 registros en total. Los percentiles están agrupados entre las cuatro zonas, no calculados por separado.
se usaron los percentiles 33,33 y 66,67, con interpolación lineal y redondeo a dos decimales
'''


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

def get_lab_chroma(a: float, b: float) -> tuple[float, float]:

    chroma = math.sqrt(a**2 + b**2)
    hue_angle = math.degrees(math.atan2(b, a)) % 360
    return chroma, hue_angle


def describe_color(rgb: tuple[int, int, int]) -> dict:
    hsv= rgb_to_hsv(rgb)
    lab=rgb_to_lab(rgb)

    _, a, b = lab
    c, h = get_lab_chroma(a, b)

    description = {
        "rgb": rgb,
        "hsv": hsv,
        "lab": lab,
        "chroma": c,
        "hue_angle": h,
    }

    return description


def get_value_range(skin_v, eyes_v, hair_v):
    return max(skin_v, eyes_v, hair_v) - min(skin_v, eyes_v, hair_v)

def get_lightness_range(skin_l: float, eyes_l: float, hair_l: float) -> float:
    l_max= max(skin_l, eyes_l, hair_l)
    l_min= min(skin_l, eyes_l, hair_l)

    lightness_range = l_max-l_min

    return lightness_range
def get_hue_angle_difference(h1: float, h2: float) -> float:

    abs_difference = abs(h1-h2)
    compared_difference = 360-abs_difference

    min_complementary_difference = min(abs_difference, compared_difference )

    return min_complementary_difference

def get_pairwise_lightness_differences(skin_l, eyes_l, hair_l) -> dict:

    diff_skin_eyes = abs(skin_l - eyes_l)
    diff_eyes_hair = abs(eyes_l - hair_l)
    diff_skin_hair = abs(skin_l - hair_l)

    return {
        "skin_eyes": diff_skin_eyes,
        "eyes_hair": diff_eyes_hair,
        "skin_hair": diff_skin_hair,
    }

def get_pairwise_value_differences(skin_v, eyes_v, hair_v) -> dict:

    cont_dif_skin_eyes= abs(skin_v-eyes_v)
    cont_dif_eyes_hair=abs(eyes_v-hair_v)
    cont_dif_skin_hair=abs(skin_v-hair_v)

    pairwise_value_differences = {
            "skin_eyes": cont_dif_skin_eyes,
            "eyes_hair": cont_dif_eyes_hair,
            "skin_hair":cont_dif_skin_hair,            
            }
            
    return pairwise_value_differences

def get_pairwise_chroma_differences(skin_c, eyes_c, hair_c) -> dict:
    cont_chrom_skin_eyes= abs(skin_c-eyes_c)
    cont_chrom_eyes_hair=abs(eyes_c-hair_c)
    cont_chrom_skin_hair=abs(skin_c-hair_c)
    
    pairwise_chrom_differences = {
        "skin_eyes": cont_chrom_skin_eyes,
        "eyes_hair": cont_chrom_eyes_hair,
        "skin_hair":cont_chrom_skin_hair,            
        }
                
    return pairwise_chrom_differences

def get_pairwise_hue_differences(skin_h, eyes_h, hair_h) -> dict:
    cont_hue_skin_eyes= get_hue_angle_difference(skin_h, eyes_h)
    cont_hue_eyes_hair=get_hue_angle_difference(eyes_h,hair_h)
    cont_hue_skin_hair=get_hue_angle_difference(skin_h,hair_h)
        
    pairwise_hue_differences = {
        "skin_eyes": cont_hue_skin_eyes,
        "eyes_hair": cont_hue_eyes_hair,
        "skin_hair":cont_hue_skin_hair,            
        }
                    
    return pairwise_hue_differences

def describe_lab_chroma(a: float, b: float) -> dict:
    
    chroma_and_angle = get_lab_chroma(a, b)
    calculated_angle = chroma_and_angle[1]
    calculated_chroma = chroma_and_angle[0]

    if a > 0:
        res_a = "Red trend"
    elif a < 0:
        res_a = "Green trend"
    else:
        res_a = "No specific direction"

    if b > 0:
        res_b = "Yellow trend"
    elif b < 0:
        res_b = "Blue trend"
    else: 
        res_b = "No specific direction"


    lab_chroma_details = {
            "a": a,
            "b": b,
            "chroma": calculated_chroma,
            "a_direction": res_a,
            "b_direction": res_b,
            "hue_angle": calculated_angle,            
            }
                    
    return lab_chroma_details
def classify_season(skin: dict, eyes: dict, hair: dict) -> dict:

    temperature_delta = skin["lab"][2] - skin["lab"][1]

    if temperature_delta > 0:
        temperature = "warm"
    elif temperature_delta < 0:
        temperature = "cool"
    else:
        temperature = "undetermined"

    lightness = classify_lightness(skin["lab"][0])
    chroma = classify_chroma(skin["chroma"])

    if temperature == "warm":
        season = "Primavera" if lightness == "light" else "Otoño"
    elif temperature == "cool":
        season = "Verano" if lightness == "light" else "Invierno"
    else:
        season = "No determinada"

    lightness_values = [
        skin["lab"][0],
        eyes["lab"][0],
        hair["lab"][0],
    ]

    high_contrast = (
        max(lightness_values) - min(lightness_values)
    ) >= 20

    expects_high_contrast = season in (
        "Primavera",
        "Invierno"
    )
    contrast_matches = (
        high_contrast == expects_high_contrast
    )

    expected_chroma = {
        "Primavera": "intense",
        "Verano": "soft",
        "Otoño": "soft",
        "Invierno": "intense",
    }
    chroma_matches = (
        chroma == expected_chroma.get(season)
    )

    if (
        temperature == "undetermined"
        or season == "No determinada"
        or abs(temperature_delta) <= 3
    ):
        rule_consistency = "low"
    elif contrast_matches and chroma_matches:
        rule_consistency = "high"
    elif contrast_matches or chroma_matches:
        rule_consistency = "medium"
    else:
        rule_consistency = "low"

    return {
        "temperature_delta": temperature_delta,
        "temperature": temperature,
        "lightness": lightness,
        "chroma": chroma,
        "season": season,
        "rule_consistency": rule_consistency,
    }

def analyze_color_relationships(skin_rgb: tuple[int, int, int], eyes_rgb: tuple[int, int, int], hair_rgb: tuple[int, int, int]) -> dict:
    # La estación usa categorías de piel; ojos y cabello aportan contraste.
    skin = describe_color(skin_rgb)
    eyes = describe_color(eyes_rgb)
    hair = describe_color(hair_rgb)

    #chromatic descriptions
    skin_chroma = describe_lab_chroma(skin["lab"][1], skin["lab"][2])
    eyes_chroma = describe_lab_chroma(eyes["lab"][1], eyes["lab"][2])
    hair_chroma = describe_lab_chroma(hair["lab"][1], hair["lab"][2])

    skin_l = skin["lab"][0]
    skin_v = skin["hsv"][2]
    skin_c = skin["chroma"]
    skin_h =skin["hue_angle"]

    eyes_l = eyes["lab"][0]
    eyes_v = eyes["hsv"][2]
    eyes_c = eyes["chroma"]
    eyes_h = eyes["hue_angle"]

    hair_l = hair["lab"][0]
    hair_v = hair["hsv"][2]
    hair_c = hair["chroma"]
    hair_h = hair["hue_angle"]

    # contrasts and differences
    value_range = get_value_range(skin_v, eyes_v, hair_v)
    lightness_range = get_lightness_range(skin_l, eyes_l, hair_l)
    seasonal_analysis = classify_season(skin, eyes, hair)
    pairwise_lightness_differences = get_pairwise_lightness_differences(skin_l, eyes_l, hair_l)
    pairwise_value_differences=get_pairwise_value_differences(skin_v, eyes_v, hair_v)
    pairwise_chroma_differences = get_pairwise_chroma_differences(skin_c, eyes_c, hair_c)
    pairwise_hue_differences = get_pairwise_hue_differences(skin_h, eyes_h, hair_h)

    colors_relationships= {
        "skin": skin,
        "eyes": eyes,
        "hair":hair,
        "skin_chroma": skin_chroma,
        "eyes_chroma": eyes_chroma,
        "hair_chroma": hair_chroma,
        "color_ranges": {
            "value": value_range,
            "lightness": lightness_range
        },
        "pairwise_lightness_differences": pairwise_lightness_differences,
        "pairwise_value_differences": pairwise_value_differences,
        "pairwise_chroma_differences": pairwise_chroma_differences,
        "pairwise_hue_differences": pairwise_hue_differences,
        "seasonal_analysis": seasonal_analysis,
    }

    
    return colors_relationships


def classify_lightness(l_value):
    # Referencia de piel: 150 sujetos del origen 1 (UK), medidos en mejilla, pómulo,
    # mentón y frente. Los 600 valores agrupados usan percentiles lineales 33,33/66,67,
    # redondeados a dos decimales. Ojos y cabello no se calibraron por separado.
    if l_value <= 60.33:
        return "dark"
    elif l_value <= 64.32:
        return "medium"
    else:
        return "light"
def classify_chroma(c_value):
    if c_value <= 20.04:
        return "soft"
    elif c_value <= 22.05:
        return "medium"
    else:
        return "intense"