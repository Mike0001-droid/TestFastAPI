from typing import Optional

from pydantic import BaseModel
from dataclasses import field


class BuildingSchema(BaseModel):
    id: int
    city: str
    street: str
    house_number: int
    apartment_number: int
    width: float
    longitude: float

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    id: int
    name: str
    category_id: int

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    id: int
    name: str
    activity_id: int
    products: list[ProductSchema] = field(default_factory=list)

    class Config:
        from_attributes = True


class ActivitySchema(BaseModel):
    id: int
    name: str
    organization_id: int
    categories: list[CategorySchema] = field(default_factory=list)

    class Config:
        from_attributes = True

class OrganizationSchema(BaseModel):
    id: int
    name: str
    phone: str
    building_id: int
    buildings: BuildingSchema = field(default_factory=list)
    activities: list[ActivitySchema] = field(default_factory=list)
    class Config:
        from_attributes = True

