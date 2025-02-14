from sqlalchemy import UniqueConstraint
from .base import Base
from .mixins.int_id_pk import IntIdPkMixin, NameAndIntIdPkMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship



class Organization(NameAndIntIdPkMixin, Base):
    phone: Mapped[str]
    buildings: Mapped[list["Building"]] = relationship(
        back_populates="organization", uselist=False
    )
    activities: Mapped[list["Activity"]] = relationship(
        back_populates="organization"
    )

    building_id: Mapped[int] = (
        mapped_column(ForeignKey("buildings.id", ondelete="CASCADE"))
    )

    __table_args__ = (
        UniqueConstraint("name", "phone"),
    )


class Building(IntIdPkMixin, Base):
    city: Mapped[str]
    street: Mapped[str]
    house_number: Mapped[int]
    apartment_number: Mapped[int]
    width: Mapped[float]
    longitude: Mapped[float]

    organization: Mapped[list["Organization"]] = relationship(
        back_populates="buildings",
    )


class Activity(NameAndIntIdPkMixin, Base):

    organization_id: Mapped[int] = (
        mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"))
    )

    organization: Mapped[list["Organization"]] = relationship(
        back_populates="activities"
    )
    categories: Mapped[list["Category"]] = relationship(
        back_populates="activity"
    )


class Category(NameAndIntIdPkMixin, Base):
    activity_id: Mapped[int] = mapped_column(ForeignKey("activitys.id", ondelete="CASCADE"))

    activity: Mapped[list["Activity"]] = relationship(
        back_populates="categories"
    )
    products: Mapped[list["Product"]] = relationship(
        back_populates="category"
    )


class Product(NameAndIntIdPkMixin, Base):
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id", ondelete="CASCADE"))

    category: Mapped[list["Category"]] = relationship(
        back_populates="products"
    )