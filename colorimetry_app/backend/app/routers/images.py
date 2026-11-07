"""
Image management endpoints.

They only delegate to `ImageService` (core) and return its result: the domain
errors are translated to HTTP by the exception handler in `app/errors.py`.
"""

from fastapi import APIRouter, Depends, File, UploadFile, status #permite agrupar endpoints relacionados. permite inyectar dependencias, en este caso el servicio. status: proporciona constantes para los códigos HTTP

from app.core.service import ImageService ImageService# contiene la lógica que coordina el procesamiento.
from app.dependencies import get_image_service #revisar
from app.schemas import ErrorResponse, ImageOut #error response revisar

router = APIRouter(prefix="/api", tags=["analysis"]) #todos los endpoints de este router empiezan con /api/images.

ERROR_RESPONSES = {#revisar
    404: {"model": ErrorResponse, "description": "IMAGE_NOT_FOUND: the image does not exist"},
    501: {"model": ErrorResponse, "description": "NOT_IMPLEMENTED"},
}


@router.post(
    "",
    rresponse_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "UNSUPPORTED_FORMAT or INVALID_FILE"},
        413: {"model": ErrorResponse, "description": "FILE_TOO_LARGE: exceeds MAX_SIZE_BYTES"},
        501: ERROR_RESPONSES[501],
    },
    summary="Upload an image",
)

#adaptar
def upload_image(file: UploadFile = File(...), service: ImageService = Depends(get_image_service)):
    """Stores the file in STORAGE_DIR with a unique name and records its URL in the database.

    Validations, in this order:
      1. size > MAX_SIZE_BYTES                   -> 413 FILE_TOO_LARGE
      2. the content does not open as an image   -> 400 INVALID_FILE (includes empty file)
      3. format not in ALLOWED_FORMATS           -> 400 UNSUPPORTED_FORMAT (e.g. GIF, TIFF)
    The format is detected by the content, not by the extension or the content-type.
    """
    return service.upload(file.filename or "image", file.file)



'''
Por ahora no son necesarios 
@router.get("", response_model=list[ImageOut], responses=ERROR_RESPONSES, summary="List images")
def list_images(service: ImageService = Depends(get_image_service)):
    """Returns all the images (originals and results) ordered by descending id."""
    return service.list()


@router.get("/{image_id}", response_model=ImageOut, responses=ERROR_RESPONSES, summary="Get an image")
def get_image(image_id: int, service: ImageService = Depends(get_image_service)):
    return service.get(image_id)


@router.delete(
    "/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=ERROR_RESPONSES,
    summary="Delete an image",
)
def delete_image(image_id: int, service: ImageService = Depends(get_image_service)):
    """Deletes the record and the file from disk. Derived images are kept with source_id = null."""
    service.delete(image_id)'''

