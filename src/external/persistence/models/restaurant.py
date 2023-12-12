from sqlalchemy import Uuid, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.external.persistence.databases import sqlalchemy_db as db


class RestaurantModel(db.Model):
    __tablename__ = "restaurant"
    id: Mapped[str] = mapped_column(Uuid, primary_key=True)
    rating: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    site: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    street: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    state: Mapped[str] = mapped_column(String)
    lat: Mapped[float] = mapped_column(Float)
    lng: Mapped[float] = mapped_column(Float)
