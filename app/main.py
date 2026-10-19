from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.v1 import api_v1_router
from app.core.config import settings
from app.core.error_handlers import register_exception_handlers
from app.schemas.response import SuccessResponse

app = FastAPI(
    title="Dynamic Form API",
    description="Clean Architecture Dynamic Form Backend in Python / FastAPI",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_ALLOWED_METHODS,
    allow_headers=settings.CORS_ALLOWED_HEADERS,
)

app.include_router(api_v1_router)


@app.get("/api/health", response_model=SuccessResponse[dict])
async def health_check():
    return SuccessResponse.create(
        data={"status": "healthy"},
        message="Dynamic Form Python API is ready",
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=(settings.ENVIRONMENT == "development"),
    )