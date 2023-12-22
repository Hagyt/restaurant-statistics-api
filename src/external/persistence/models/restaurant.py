from sqlalchemy import Uuid, String, Integer, Float
from geoalchemy2 import Geometry
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
    _geom: Mapped[Geometry] = mapped_column(Geometry(geometry_type='POINT', srid=4326), name="geom")


    @property
    def geom(self):
        """The geom property"""
        return self._geom
    

    @geom.setter
    def geom(self, geom: dict):
        lng = geom.get('lng')
        lat = geom.get('lat')
        self._geom = f'SRID=4326;POINT({lng} {lat})'


    def update(self, db, data, commit=True):

        for attr, value in data.items():
            setattr(self, attr, value)

        if commit:
            db.session.commit()

    
    def delete(self, db, commit=True):
        db.session.delete(self)

        if commit:
            db.session.commit()
