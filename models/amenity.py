#!/usr/bin/python3
"""Amenity class module"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Amenity(BaseModel):
    """Amenity class"""
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)
