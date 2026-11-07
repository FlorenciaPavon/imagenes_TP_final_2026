"""FastAPI dependencies: build the core objects for each request."""

from fastapi import Depends

from app.core.imaging import ImageCodec 
from app.core.service import ImageService
