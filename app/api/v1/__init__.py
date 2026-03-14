from fastapi import APIRouter
from app.api.v1 import asr

api_router = APIRouter(prefix="/v1")

api_router.include_router(asr.router, prefix="/asr", tags=["ASR"])
