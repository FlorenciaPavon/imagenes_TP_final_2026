
"""
Image analysis endpoints.
"""

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from pydantic import ValidationError

from app.config import MAX_SIZE_BYTES
from app.core.exceptions import FileTooLarge, InvalidParameters
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
            "description": "INVALID_FILE, UNSUPPORTED_FORMAT, INVALID_PARAMETERS or INVALID_COORDINATES",
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
    content = await file.read(MAX_SIZE_BYTES + 1)
    if len(content) > MAX_SIZE_BYTES:
        raise FileTooLarge(MAX_SIZE_BYTES)

    try:
        selections = Selections.model_validate_json(selections_json)
    except ValidationError as exc:
        raise InvalidParameters(
            "Selections must be valid JSON with non-negative x/y coordinates for skin, eyes, and hair."
        ) from exc

    return service.analyze(content, selections)
