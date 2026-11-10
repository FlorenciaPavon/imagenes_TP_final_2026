"""
Use cases of the application: image analysis.

"""

#from app import config
from app.core.exceptions import UnsupportedFormat, InvalidCoordinates
from app.core.imaging import ImageCodec
from app.schemas import Selections, AnalysisResponse
from app.core.palette import analyze_color_relationships
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

        color_relationships = analyze_color_relationships(skin_color, eyes_color,hair_color) 

        print(color_relationships.keys())

        return color_relationships #a cambiar mas tarde, el return debe ser AnalysisResponse


print(AnalysisService.analyze)