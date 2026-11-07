"""
API contract 
The structure is:

AnalysisResponse
colors
Extracted colors from the original photo
- skin
- eyes
- hair

analysis
Chromatic features
- temperature
- luminosity
- contrast

Palette
recommended palette
- name
- colors
"""


from typing import Literal

from pydantic import BaseModel, Field

#Supported image formats
ImageFormat = Literal["PNG", "JPEG", "WEBP", "BMP"]

ErrorCode = Literal[
    "INVALID_FILE",
    "UNSUPPORTED_FORMAT",
    "FILE_TOO_LARGE",
    "INVALID_PARAMETERS", #Los datos recibidos no cumplen alguna regla del análisis. Reglas de negocio
    "INVALID_COORDINATES", #	Alguna coordenada está fuera de los límites de la imagen.
]

Temperature = Literal["warm", "cool", "neutral"] #Literal restringe los valores permitidos. En cambio, si usamos str, acepta cualquier texto, incluso uno que no tenga sentido para nuestro análisis.

Luminosity = Literal["light", "medium", "dark"]

Contrast = Literal["low", "medium", "high"]

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

'''Muestra la paleta recomendada como resultado'''
class Palette(BaseModel): #validamos que exista al menos un color. También se puede agregar una validación específica para asegurar que cada texto tenga formato hexadecimal
    name: str 
    colors: list[str] = Field(..., min_length=1) #### A MEJORAR

'''Ej
Palette(
    name="Otoño suave",
    colors=["#A66F50", "#C18C69", "#D5B68C"]
)
'''
class ColorAnalysis(BaseModel):
    temperature: Temperature
    luminosity: Luminosity
    contrast: Contrast   

#respuesta provisoria de analisis
class AnalysisResponse(BaseModel):
    colors: ExtractedColors
    analysis: ColorAnalysis
    palette: Palette

class ErrorDetail(BaseModel):
    code: ErrorCode
    message: str = Field(description="Message for the user") 

class ErrorResponse(BaseModel):
   """Body of all custom error responses."""
    detail: ErrorDetail
