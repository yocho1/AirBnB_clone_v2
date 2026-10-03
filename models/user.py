#!/usr/bin/python3
"""User class module"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel):
    """User class"""
    __tablename__ = 'users'

    email = Column(String(128), nullable=False, default="")
    password = Column(String(128), nullable=False, default="")
    first_name = Column(String(128), nullable=True, default="")
    last_name = Column(String(128), nullable=True, default="")

    places = relationship("Place", backref="user", cascade="all, delete")
    reviews = relationship("Review", backref="user", cascade="all, delete")
