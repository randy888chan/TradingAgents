from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router as api_v1_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

app.include_router(api_v1_router, prefix=settings.API_V1_STR)
