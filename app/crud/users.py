
from core.models.models import Organization, Activity, Category, Building
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession


def options_for_organizations():
    return select(Organization).options(
selectinload(Organization.buildings),
        selectinload(Organization.activities)
        .selectinload(Activity.categories)
        .selectinload(Category.products)
    )

async def get_organization_by_id(session: AsyncSession, organization_id: int):
    result = await session.execute(
        options_for_organizations().filter(
            Organization.id == organization_id
        )
    )
    organization = result.scalars().first()
    return organization


async def get_organization_by_building(session: AsyncSession, building_id: int):
    result = await session.execute(
        options_for_organizations().filter(
            Organization.building_id == building_id
        )
    )
    organization = result.scalars().first()
    return organization


async def get_organization_by_activity(session: AsyncSession, activity_id: int):
    result = await session.execute(
        options_for_organizations().join(Activity)
        .filter(Activity.id == activity_id)
    )
    organization = result.scalars().all()
    return organization


async def get_organization_in_radius(
        session: AsyncSession, width, longitude, radius
    ):
    result = await session.execute(options_for_organizations().join(Building)
        .filter(and_(
            Building.width.between(width - radius, width + radius),
            Building.longitude.between(longitude - radius, longitude + radius)
            )
        )
    )
    organization = result.scalars().all()
    return organization


async def get_organization_by_name(
        session: AsyncSession, name
    ):
    result = await session.execute(options_for_organizations()
        .filter(Organization.name == name)
    )
    organization = result.scalars().all()
    return organization


async def get_organization_by_activity_name(
        session: AsyncSession, activity_name: str
    ):

    result = await session.execute(
        options_for_organizations().join(Activity)
        .where(Activity.name.ilike(f"%{activity_name}%"))
    )
    organizations = result.scalars().all()
    return organizations