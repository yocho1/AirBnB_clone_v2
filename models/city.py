#!/usr/bin/python3
"""City class"""
import os
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """City class"""
    __tablename__ = "cities"
    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        state_id = Column(String(60), ForeignKey("states.id"),
                          nullable=False)
        name = Column(String(128), nullable=False)
    else:
        state_id = ""
        name = ""
