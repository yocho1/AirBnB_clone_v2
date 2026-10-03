#!/usr/bin/python3
"""BaseModel class module"""

from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """Base class for all AirBnB models"""
    __abstract__ = True

    id = Column(String(60), primary_key=True,
                default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance"""
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key in ['created_at', 'updated_at']:
                    if isinstance(value, str):
                        value = datetime.fromisoformat(value)
                setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            from models import storage
            storage.new(self)

    def __str__(self):
        """String representation"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Update updated_at and save to storage"""
        self.updated_at = datetime.now()
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert to dictionary for serialization"""
        dict_copy = self.__dict__.copy()
        dict_copy['__class__'] = self.__class__.__name__
        if isinstance(dict_copy.get('created_at'), datetime):
            dict_copy['created_at'] = self.created_at.isoformat()
        if isinstance(dict_copy.get('updated_at'), datetime):
            dict_copy['updated_at'] = self.updated_at.isoformat()
        dict_copy.pop('_sa_instance_state', None)
        return dict_copy

    def delete(self):
        """Delete the current instance from storage"""
        from models import storage
        storage.delete(self)
