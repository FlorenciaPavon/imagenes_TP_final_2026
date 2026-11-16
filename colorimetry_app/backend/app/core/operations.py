"""
Color extraction operations.

"""
from statistics import median

def get_region_pixels(image, x: int, y: int, radius: int = 2) -> list:
    """
    Obtiene los píxeles de una región de 5x5 alrededor del punto seleccionado.
    """

    x_inicio = max(0, x - radius)
    x_fin = min(image.width, x + radius + 1)

    y_inicio = max(0, y - radius)
    y_fin = min(image.height, y + radius + 1)    

    pixels = []

    for row in range(y_inicio, y_fin):
        for col in range(x_inicio, x_fin):
            pixel = image.getpixel((col, row))
            pixels.append(pixel)
        

    return pixels

def get_representative_color(image, x: int, y: int, radius: int = 2) -> tuple[int, int, int]:
    image = image.convert("RGB") #que pasa con los grises?
    pixels = get_region_pixels(image, x, y, radius)

    reds = []
    greens = []
    blues = []

    for pixel in pixels:
        reds.append(pixel[0])
        greens.append(pixel[1])
        blues.append(pixel[2])  

    median_red = round(median(reds))
    median_green =round(median(greens))
    median_blue = round(median(blues))

    representative_color = (median_red, median_green, median_blue)
    return representative_color




