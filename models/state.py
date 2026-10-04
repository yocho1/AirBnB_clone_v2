#!/usr/bin/python3
"""State class"""
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """State class"""
    __tablename__ = "states"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            """Cities of this state (FileStorage)"""
            from models.city import City
            return [c for c in models.storage.all(City).values()
                    if c.state_id == self.id]
