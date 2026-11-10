
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import FRONTEND_DIR
from app.errors import register_exception_handlers
from app.routers import images



app = FastAPI(
    title="Personal Colorimetry API",
    description="API for personal color analysis based on selected skin, eye and hair colors.",
    version="1.0.0",
)
# Allows opening the frontend from another origin (e.g. Live Server on :5500).
app.add_middleware(
    CORSMiddleware, #adaptar
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)


@app.get("/api/health", tags=["system"], summary="Server status")
def health():
    return {"status": "ok"}


app.include_router(images.router)


# Frontend (must be mounted last because it captures "/").
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
