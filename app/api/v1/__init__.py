from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.fields import router as fields_router
from app.api.v1.forms import router as forms_router
from app.api.v1.submissions import router as submissions_router

api_v1_router = APIRouter(prefix="/api")

api_v1_router.include_router(auth_router)
api_v1_router.include_router(forms_router)
api_v1_router.include_router(fields_router)
api_v1_router.include_router(submissions_router)

__all__ = ["api_v1_router"]
