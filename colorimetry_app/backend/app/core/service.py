"""
Use cases of the application: image analysis.

"""

from app import config
from app.core.exceptions import UnsupportedFormat
from app.core.imaging import ImageCodec
from app.schemas import Selections, AnalysisResponse


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
            pass  # Aquí nos quedamos.