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
    h = math.degrees(math.atan2(b, a)) % 360
    list_crhom.append(h)

    return tuple(list_crhom)


def describe_color(rgb: tuple[int, int, int]) -> dict:
    hsv= rgb_to_hsv(rgb)
    lab=rgb_to_lab(rgb)

    l, a, b = lab
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

def get_luminosity_contrast(skin_l: float, eyes_l: float, hair_l: float) -> float:
    l_max= max(skin_l, eyes_l, hair_l)
    l_min= min(skin_l, eyes_l, hair_l)

    contrast = l_max-l_min

    return contrast
def get_hue_angle_difference(h1: float, h2: float) -> float:

    abs_difference = abs(h1-h2)
    compared_difference = 360-abs_difference

    min_complementary_difference = min(abs_difference, compared_difference )

    return min_complementary_difference

def get_pairwise_luminosity_differences(skin_l, eyes_l, hair_l) -> dict:

    lum_dif_skin_eyes= abs(skin_l-eyes_l)
    lum_dif_eyes_hair=abs(eyes_l-hair_l)
    lum_dif_skin_hair=abs(skin_l-hair_l)

    pairwise_luminosity_differences = {
            "skin_eyes": lum_dif_skin_eyes,
            "eyes_hair": lum_dif_eyes_hair,
            "skin_hair":lum_dif_skin_hair,            
            }
            
    return pairwise_luminosity_differences

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

def get_pairwise_chromaticity_differences(skin_c, eyes_c, hair_c) -> dict:
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

def describe_lab_chromaticity(a: float, b: float) -> dict:  
    
    chromaticity = get_lab_chromaticity(a,b)
    calculated_angle = chromaticity[1]
    calculated_chromaticity=chromaticity[0]

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


    lab_chromaticity_details = {
            "a": a,
            "b": b,
            "chromaticity": calculated_chromaticity,
            "a_direction": res_a,
            "b_direction": res_b,
            "hue_angle": calculated_angle,            
            }
                    
    return lab_chromaticity_details
  

def analyze_color_relationships(skin_rgb: tuple[int, int, int], eyes_rgb: tuple[int, int, int], hair_rgb: tuple[int, int, int]) -> dict:
    #individual colors
    skin = describe_color(skin_rgb)
    eyes = describe_color(eyes_rgb)
    hair = describe_color(hair_rgb)
    #chromatic descriptions
    skin_chromaticity = describe_lab_chromaticity(skin["lab"][1], skin["lab"][2])
    eyes_chromaticity = describe_lab_chromaticity(eyes["lab"][1], eyes["lab"][2])
    hair_chromaticity = describe_lab_chromaticity(hair["lab"][1], hair["lab"][2])

    skin_l = skin["lab"][0]
    skin_v = skin["hsv"][2]
    skin_c= skin["chromaticity"] 
    skin_h =skin["hue_angle"]

    eyes_l = eyes["lab"][0]
    eyes_v = eyes["hsv"][2]
    eyes_c = eyes["chromaticity"]
    eyes_h = eyes["hue_angle"]

    hair_l = hair["lab"][0]
    hair_v = hair["hsv"][2]
    hair_c = hair["chromaticity"]
    hair_h = hair["hue_angle"]

    # contrasts and differences
    hsv_contrast = contrast(skin_v,eyes_v,hair_v)
    lab_contrast= get_luminosity_contrast(skin_l,eyes_l,hair_l)
    pairwise_luminosity_differences= get_pairwise_luminosity_differences(skin_l, eyes_l, hair_l)
    pairwise_value_differences=get_pairwise_value_differences(skin_v, eyes_v, hair_v)
    pairwise_chrom_differences = get_pairwise_chromaticity_differences(skin_c, eyes_c, hair_c)
    pairwise_hue_differences = get_pairwise_hue_differences(skin_h, eyes_h, hair_h)

    colors_relationships= {
        "skin": skin,
        "eyes": eyes,
        "hair":hair,
        "skin_chromaticity": skin_chromaticity,
        "eyes_chromaticity": eyes_chromaticity,
        "hair_chromaticity": hair_chromaticity,
        "luminosity_contrast": {
            "hsv": hsv_contrast,
            "lab": lab_contrast
        },
        "pairwise_luminosity_differences": pairwise_luminosity_differences,
        "pairwise_value_differences": pairwise_value_differences,
        "pairwise_chrom_differences": pairwise_chrom_differences,
        "pairwise_hue_differences": pairwise_hue_differences
    }
    return colors_relationships

