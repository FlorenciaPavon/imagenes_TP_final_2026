"""
API contract 
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

class HSVColor(BaseModel):
    h: float = Field(..., ge=0, le=1) #colorsys, trabaja con los tres componentes HSV en escala normalizada
    s: float = Field(..., ge=0, le=1)
    v: float = Field(..., ge=0, le=1)

class LabColor(BaseModel):
    l: float = Field(..., ge=0, le=100)
    a: float = Field(..., ge=-128, le=127)# corresponden a la representación LAB de Pillow. Pillow tiene precisión limitada porque trabaja con canales de 8 bits. Por eso, los valores a* y b* son enteros, aunque los esten como float en Pydantic
    b: float = Field(..., ge=-128, le=127)

class AnalyzedColor(BaseModel):
    rgb: RGBColor
    hsv: HSVColor
    lab: LabColor
    chromaticity: float = Field(..., ge=0)
    hue_angle: float = Field(..., ge=0, lt=360) 

class PairwiseDifferences(BaseModel):
    skin_eyes: float = Field(..., ge=0)
    eyes_hair: float = Field(..., ge=0)
    skin_hair: float = Field(..., ge=0)

class ColorDifferences(BaseModel):
    luminosity: PairwiseDifferences
    value: PairwiseDifferences
    chromaticity: PairwiseDifferences
    hue: PairwiseDifferences

class GlobalContrast(BaseModel):
    hsv: float = Field(..., ge=0, le=1)
    lab: float = Field(..., ge=0, le=100)

class ColorRelationships(BaseModel):
    skin: AnalyzedColor
    eyes: AnalyzedColor
    hair: AnalyzedColor
    luminosity_contrast: GlobalContrast
    pairwise_differences: ColorDifferences

    

class Palette(BaseModel): #validamos que exista al menos un color. También se puede agregar una validación específica para asegurar que cada texto tenga formato hexadecimal
    name: str 
    colors: list[str] = Field(..., min_length=1) #### A MEJORAR

class AnalysisResponse(BaseModel):
    analysis: ColorRelationships
    palette: Palette 
    
class ErrorDetail(BaseModel):
    code: ErrorCode
    message: str = Field(description="Message for the user") 

class ErrorResponse(BaseModel):
    """Body of all custom error responses."""
    detail: ErrorDetail


    
'''Ej
Palette(
    name="Otoño suave",
    colors=["#A66F50", "#C18C69", "#D5B68C"]
)

#respuesta provisoria de analisis
class AnalysisResponse(BaseModel):
    colors: ExtractedColors
    analysis: ColorAnalysis
    palette: Palette'''