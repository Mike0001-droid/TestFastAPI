from typing import Annotated
from fastapi import Query
from fastapi import (
    APIRouter,
    Depends, HTTPException,
    Security
)
from core.models import db_helper
from core.schemas.dtos import OrganizationSchema
from crud.users import (
    get_organization_by_id, get_organization_by_building,
    get_organization_by_activity, get_organization_in_radius,
    get_organization_by_name)
    #get_organization_by_activity_name
from sqlalchemy.ext.asyncio import AsyncSession
from .auth import get_api_key
router = APIRouter(tags=["Organizations"])


@router.get("/{organization_id}", response_model=OrganizationSchema)
async def organization_by_id(
        organization_id: int,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        api_key: str = Security(get_api_key),
    ):
    """
        Вывод информации об организации по её идентификатору
    """
    organization = await get_organization_by_id(session, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@router.get("/building/{building_id}", response_model=list[OrganizationSchema])
async def get_organizations_by_building(
        building_id: int,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        api_key: str = Security(get_api_key),
    ):
    """
        Список всех организаций находящихся в конкретном здании
    """
    organizations = await get_organization_by_building(session, building_id)
    if not organizations:
        raise HTTPException(status_code=404, detail="Building not found")
    return [OrganizationSchema.model_validate(org) for org in organizations]

@router.get("/activity/{activity_id}", response_model=OrganizationSchema)
async def get_organizations_by_activity(
        activity_id: int,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        api_key: str = Security(get_api_key),

    ):
    """
        Список всех организаций, которые относятся к указанному виду деятельности
    """
    organization = await get_organization_by_activity(session, activity_id)

    if not organization:
        raise HTTPException(status_code=404, detail="Building not found")

    return OrganizationSchema.model_validate(organization)


@router.get("/in_radius/", response_model=list[OrganizationSchema])
async def get_organizations_in_radius(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        api_key: str = Security(get_api_key),
        width: float = Query(..., description="Широта центральной точки"),
        longitude: float = Query(..., description="Долгота центральной точки"),
        radius: float = Query(..., description="Радиус поиска в километрах"),
    ):
    """
        Список организаций, которые находятся в заданном радиусе/прямоугольной
        области относительно указанной точки на карте. список зданий
    """
    organizations = await get_organization_in_radius(session, width, longitude, radius)

    if not organizations:
        raise HTTPException(status_code=404, detail="Organizations in radius not found")

    return [OrganizationSchema.model_validate(org) for org in organizations]


@router.get("/by_name/{name}", response_model=list[OrganizationSchema])
async def get_organizations_by_name(
        name: str,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        api_key: str = Security(get_api_key),

    ):
    """
        Поиск организации по названию
    """
    organizations = await get_organization_by_name(session, name)

    if not organizations:
        raise HTTPException(status_code=404, detail="Organizations in radius not found")

    return [OrganizationSchema.model_validate(org) for org in organizations]


# @router.get("/child_activity/{activity_name}", response_model=list[OrganizationSchema])
# async def get_organizations_by_name_activity(
#         activity_name: str,
#         session: Annotated[
#             AsyncSession,
#             Depends(db_helper.session_getter)
#         ],
#         api_key: str = Security(get_api_key),
#
#     ):
#     organizations = await get_organization_by_activity_name(session, activity_name)
#
#     if not organizations:
#         raise HTTPException(status_code=404, detail="Organizations in by name activity not found")
#
#     return [OrganizationSchema.model_validate(org) for org in organizations]
