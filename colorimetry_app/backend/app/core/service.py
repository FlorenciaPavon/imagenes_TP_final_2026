"""
Use cases of the application: image analysis.

"""

from app import config

from app.core.imaging import ImageCodec
from app.schemas import (
    Selections,
    Palette,
    RGBColor,
    HSVColor,
    LabColor,
    AnalyzedColor,
    GlobalContrast,
    ColorDifferences,
    ColorRelationships,
    AnalysisResponse
)
from app.core.palette import analyze_color_relationships
from app.core.operations import get_representative_color
from app.core.exceptions import (
    UnsupportedFormat,
    InvalidCoordinates,
    FileTooLarge,
)

def _build_analyzed_color(color_data: dict) -> AnalyzedColor:
    analyzed = AnalyzedColor(
        rgb=RGBColor(
            r=color_data["rgb"][0],
            g=color_data["rgb"][1],
            b=color_data["rgb"][2]
        ),
        hsv=HSVColor(
            h=color_data["hsv"][0],
            s=color_data["hsv"][1],
            v=color_data["hsv"][2]
        ),
        lab=LabColor(
            l=color_data["lab"][0],
            a=color_data["lab"][1],
            b=color_data["lab"][2]
        ),
        chromaticity=color_data["chromaticity"],
        hue_angle=color_data["hue_angle"]
    )

    return analyzed

class AnalysisService:
    def __init__(self, codec: ImageCodec):
        self._codec = codec

    def analyze(self, content: bytes, selections: Selections) -> AnalysisResponse:
        
        if len(content) > config.MAX_SIZE_BYTES:
            raise FileTooLarge(config.MAX_SIZE_BYTES)
        
        info = self._codec.inspect(content)

        if info.format not in config.ALLOWED_FORMATS:
            raise UnsupportedFormat(info.format)

        image = self._codec.open(content)

        points = (selections.skin, selections.eyes, selections.hair)

        for point in points:
            if point.x >= info.width or point.y >= info.height:
                raise InvalidCoordinates(
                    point.x,
                    point.y,
                    info.width,
                    info.height
                )

        skin_color = get_representative_color(image, selections.skin.x, selections.skin.y)

        eyes_color = get_representative_color(image, selections.eyes.x, selections.eyes.y)

        hair_color = get_representative_color(image, selections.hair.x, selections.hair.y)

        color_relationships = analyze_color_relationships(skin_color, eyes_color,hair_color) 

        pairwise_differences = {
            "luminosity": color_relationships["pairwise_luminosity_differences"],
            "value": color_relationships["pairwise_value_differences"],
            "chromaticity": color_relationships["pairwise_chrom_differences"],
            "hue": color_relationships["pairwise_hue_differences"]
        }

        relationships = ColorRelationships(
            skin=_build_analyzed_color(color_relationships["skin"]),
            eyes=_build_analyzed_color(color_relationships["eyes"]),
            hair=_build_analyzed_color(color_relationships["hair"]),
            luminosity_contrast=GlobalContrast(
                hsv=color_relationships["luminosity_contrast"]["hsv"],
                lab=color_relationships["luminosity_contrast"]["lab"]
            ),
            pairwise_differences=ColorDifferences(**pairwise_differences)
        )

        palette = Palette(
            name="Colores analizados",
            colors=[
                f"#{relationships.skin.rgb.r:02X}{relationships.skin.rgb.g:02X}{relationships.skin.rgb.b:02X}",
                f"#{relationships.eyes.rgb.r:02X}{relationships.eyes.rgb.g:02X}{relationships.eyes.rgb.b:02X}",
                f"#{relationships.hair.rgb.r:02X}{relationships.hair.rgb.g:02X}{relationships.hair.rgb.b:02X}"
            ]
)
        return AnalysisResponse(
            analysis=relationships,
            palette=palette
        )
