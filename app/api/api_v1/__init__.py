from fastapi import APIRouter

from core.config import settings

from .organizations import router as organizations_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    organizations_router,
    prefix=settings.api.v1.organizations,
)
