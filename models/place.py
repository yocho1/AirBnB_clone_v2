#!/usr/bin/python3
"""Place class"""
import os
from sqlalchemy import (Column, String, Integer, Float, ForeignKey,
                        Table)
from sqlalchemy.orm import relationship
import models
from models.base_model import BaseModel, Base

if os.getenv("HBNB_TYPE_STORAGE") == "db":
    place_amenity = Table(
        "place_amenity", Base.metadata,
        Column("place_id", String(60), ForeignKey("places.id"),
               primary_key=True, nullable=False),
        Column("amenity_id", String(60), ForeignKey("amenities.id"),
               primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """Place class"""
    __tablename__ = "places"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey("cities.id"),
                         nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"),
                         nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship("Review", backref="place",
                               cascade="all, delete-orphan")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False)

        def __init__(self, *args, **kwargs):
            """Initialize with an empty amenity_ids list"""
            super().__init__(*args, **kwargs)
            self.amenity_ids = []
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Reviews of this place (FileStorage)"""
            from models.review import Review
            return [r for r in models.storage.all(Review).values()
                    if r.place_id == self.id]

        @property
        def amenities(self):
            """Amenities of this place (FileStorage)"""
            from models.amenity import Amenity
            return [a for a in models.storage.all(Amenity).values()
                    if a.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Add an Amenity"""
            from models.amenity import Amenity
            if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
