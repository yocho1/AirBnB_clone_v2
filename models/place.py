#!/usr/bin/python3
"""Place class module"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'), primary_key=True),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True))


class Place(BaseModel):
    """Place class"""
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'),
                     nullable=False, default="")
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False, default="")
    name = Column(String(128), nullable=False, default="")
    description = Column(String(1024), nullable=True, default="")
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True, default=0.0)
    longitude = Column(Float, nullable=True, default=0.0)

    reviews = relationship("Review", backref="place", cascade="all, delete")
    amenities = relationship("Amenity", secondary=place_amenity,
                             viewonly=False)
