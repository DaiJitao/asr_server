from app.api.v1 import api_router as v1_router


from fastapi import APIRouter
router = APIRouter()

router.include_router(v1_router)