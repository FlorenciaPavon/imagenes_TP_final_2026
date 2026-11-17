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
    "INVALID_PARAMETERS", 
    "INVALID_COORDINATES", 
]

Temperature = Literal["warm", "cool", "undetermined"] 

Lightness = Literal["light", "medium", "dark"]

Chroma = Literal["soft", "medium", "intense"]

RuleConsistency = Literal["low", "medium", "high"]

Season = Literal[
    "Primavera",
    "Verano",
    "Otoño",
    "Invierno",
    "No determinada"
]

class PointSelection(BaseModel):
    x: int = Field(..., ge=0) 
    y: int = Field(..., ge=0)

class Selections(BaseModel):
    skin: PointSelection
    eyes: PointSelection
    hair: PointSelection

class RGBColor(BaseModel):
    r: int = Field(..., ge=0, le=255) 
    g: int = Field(..., ge=0, le=255)
    b: int = Field(..., ge=0, le=255)

class HSVColor(BaseModel):
    h: float = Field(..., ge=0, le=1) 
    s: float = Field(..., ge=0, le=1)
    v: float = Field(..., ge=0, le=1)

class LabColor(BaseModel):
    l: float = Field(..., ge=0, le=100)
    a: float = Field(..., ge=-128, le=127)
    b: float = Field(..., ge=-128, le=127)

class AnalyzedColor(BaseModel):
    rgb: RGBColor
    hsv: HSVColor
    lab: LabColor
    chroma: float = Field(..., ge=0)
    hue_angle: float = Field(..., ge=0, lt=360) 

class PairwiseDifferences(BaseModel):
    skin_eyes: float = Field(..., ge=0)
    eyes_hair: float = Field(..., ge=0)
    skin_hair: float = Field(..., ge=0)

class ColorDifferences(BaseModel):
    lightness: PairwiseDifferences
    value: PairwiseDifferences
    chroma: PairwiseDifferences
    hue: PairwiseDifferences

class ColorRanges(BaseModel):
    value: float = Field(..., ge=0, le=1)
    lightness: float = Field(..., ge=0, le=100)

class ColorRelationships(BaseModel):
    skin: AnalyzedColor
    eyes: AnalyzedColor
    hair: AnalyzedColor
    color_ranges: ColorRanges
    pairwise_differences: ColorDifferences

    

class Palette(BaseModel): 
    name: str 
    colors: list[str] = Field(..., min_length=1) 

class SeasonalAnalysis(BaseModel):
    temperature_delta: float
    temperature: Temperature
    lightness: Lightness
    chroma: Chroma
    season: Season
    rule_consistency: RuleConsistency

class AnalysisResponse(BaseModel):
    analysis: ColorRelationships
    seasonal_analysis: SeasonalAnalysis
    palette: Palette
    
class ErrorDetail(BaseModel):
    code: ErrorCode
    message: str = Field(description="Message for the user") 

class ErrorResponse(BaseModel):
    """Body of all custom error responses."""
    detail: ErrorDetail

