"""
Use cases of the application: image analysis.

"""

from app import config
from app.core.exceptions import UnsupportedFormat, InvalidCoordinates
from app.core.imaging import ImageCodec
from app.schemas import Selections, AnalysisResponse, ExtractedColors, RGBColor
from app.core.operations import get_representative_color


class AnalysisService:
    def __init__(self, codec: ImageCodec):
        self._codec = codec

    def analyze(self, content: bytes, selections: Selections) -> AnalysisResponse:
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

        extracted_colors = ExtractedColors(
            skin=RGBColor(*skin_color),
            eyes=RGBColor(*eyes_color),
            hair=RGBColor(*hair_color)
        )

        return extracted_colors #a cambiar mas tarde, el return debe ser AnalysisResponse