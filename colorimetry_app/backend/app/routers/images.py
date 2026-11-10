
"""
Image analysis endpoints.
"""

from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from app.core.service import AnalysisService
from app.dependencies import get_analysis_service
from app.schemas import AnalysisResponse, Selections, ErrorResponse


router = APIRouter(prefix="/api", tags=["analysis"])


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "INVALID_FILE or UNSUPPORTED_FORMAT",
        },
        413: {
            "model": ErrorResponse,
            "description": "FILE_TOO_LARGE",
        },
    },
    summary="Analyze personal colors",
)
async def analyze_image(
    file: UploadFile = File(...),
    selections_json: str = Form(...),
    service: AnalysisService = Depends(get_analysis_service),
):
    content = await file.read()

    selections = Selections.model_validate_json(selections_json)

    return service.analyze(content, selections)
