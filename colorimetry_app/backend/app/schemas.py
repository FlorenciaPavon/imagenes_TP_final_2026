"""
API contract (input and output).

These schemas are the interface consumed by the frontend and checked by the
acceptance tests: DO NOT change field names, types or ranges. They validate the
request format (if it fails, FastAPI responds 422); the domain rules (for example,
that the kernel must be odd) are validated in the core classes and answered with 400.
"""


from typing import Literal

from pydantic import BaseModel, Field

# Name of each operation. Matches the last segment of its route

ImageFormat = Literal["PNG", "JPEG", "WEBP", "BMP"]

ErrorCode = Literal[
    "INVALID_FILE",
    "UNSUPPORTED_FORMAT",
    "FILE_TOO_LARGE",
    "INVALID_PARAMETERS", #Los datos recibidos no cumplen alguna regla del análisis. Reglas de negoocio
    "INVALID_COORDINATES", #	Alguna coordenada está fuera de los límites de la imagen.
]

Temperature = Literal["warm", "cool", "neutral"]

Luminosity = Literal["light", "medium", "dark"]

Contrast = Literal["low", "medium", "high"]

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


class ErrorDetail(BaseModel):
    code: ErrorCode
    message: str = Field(description="Message for the user")
   


class ErrorResponse(BaseModel):
    """Body of ALL custom error responses (400, 404, 413, 501)."""

class PointSelection(BaseModel):#permite que Pydantic valide los datos.
    x: int = Field(..., ge=0) #Field(...): indica que el dato es obligatorio. ge=0: significa greater than or equal to 0, es decir, mayor o igual a cero.
    y: int = Field(..., ge=0)

class Selections(BaseModel):
    skin: PointSelection
    eyes: PointSelection
    hair: PointSelection
'''no estamos declarando nuevamente x e y.

Estamos diciendo que cada atributo (skin, eyes, hair) debe ser un objeto que cumpla con la estructura de PointSelection.
por ej
selections = Selections(
    skin={"x": 250, "y": 180},
    eyes={"x": 270, "y": 130},
    hair={"x": 300, "y": 60}
)
Pydantic valida los tres puntos utilizando las mismas reglas. sino manda error 422: el formato o la estructura de los datos recibidos no cumple el esquema definido.
'''

class RGBColor(BaseModel):
    r: int = Field(..., ge=0, le=255) #0 hasta 255.
    g: int = Field(..., ge=0, le=255)
    b: int = Field(..., ge=0, le=255)


class ExtractedColors(BaseModel):
    skin: RGBColor
    eyes: RGBColor
    hair: RGBColor

'''Muestra la paleta analizada por colorimetria'''
class Palette(BaseModel): #validamos que exista al menos un color. Tambien se puede agregar una validación específica para asegurar que cada texto tenga formato hexadecimal
    name: str 
    colors: list[str] = Field(..., min_length=1)

'''Ej
Palette(
    name="Otoño suave",
    colors=["#A66F50", "#C18C69", "#D5B68C"]
)
'''

#respuesta provisoria de analisis
class AnalysisResponse(BaseModel):
    colors: ExtractedColors
    palette: Palette

