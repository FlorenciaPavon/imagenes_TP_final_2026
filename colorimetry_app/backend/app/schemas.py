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
# ---------------------------------------------------------------------------
# Input: parameters of each operation
# ---------------------------------------------------------------------------
'''CORRESPONDEN A OTRO TP
class FactorIn(BaseModel):
    """Enhancement factor. 1.0 = unchanged image."""
    factor: float = Field(1.0, ge=0.0, le=3.0)


class BrightnessIn(FactorIn):
    """0 = black, 1.0 = unchanged."""


class ContrastIn(FactorIn):
    """0 = uniform gray, 1.0 = unchanged."""


class SaturationIn(FactorIn):
    """0 = no color (R = G = B), 1.0 = unchanged."""


class SharpnessIn(BaseModel):
    """<1 smooths, 1.0 = unchanged, >1 sharpens."""
    factor: float = Field(1.0, ge=0.0, le=5.0)


class BlurIn(BaseModel):
    method: Literal["gaussian", "median", "average"] = "gaussian"
    kernel_size: int = Field(5, ge=1, le=51, description="Kernel side in pixels. Domain rule: odd.")


class EdgesIn(BaseModel):
    lower_threshold: int = Field(100, ge=0, le=255, description="Domain rule: lower than upper_threshold.")
    upper_threshold: int = Field(200, ge=0, le=255)


class RotationIn(BaseModel):
    angle: float = Field(90.0, ge=-360.0, le=360.0, description="Degrees. Positive = counterclockwise.")
    expand: bool = Field(True, description="Enlarge the canvas so the image does not get cropped")


class MirrorIn(BaseModel):
    direction: Literal["horizontal", "vertical"] = Field(
        "horizontal", description="horizontal = left↔right, vertical = top↔bottom"
    )


class ResizeIn(BaseModel):
    width: int = Field(..., ge=1, le=8000)
    height: int | None = Field(
        None, ge=1, le=8000,
        description=(
            "Ignored if keep_aspect_ratio is true (computed as round(width * orig_height / orig_width)). "
            "Domain rule: required if keep_aspect_ratio is false."
        ),
    )
    keep_aspect_ratio: bool = True'''
