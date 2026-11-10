"""FastAPI dependencies: build the core objects for each request."""

from app.core.imaging import ImageCodec
from app.core.service import AnalysisService


def get_analysis_service() -> AnalysisService:
    codec = ImageCodec()
    return AnalysisService(codec)