#!/usr/bin/python3
"""BaseModel class"""
import os
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

DB = os.getenv("HBNB_TYPE_STORAGE") == "db"
if DB:
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """Base class for all models"""
    if DB:
        id = Column(String(60), primary_key=True, nullable=False)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow)
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialize a new instance"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ("created_at", "updated_at") and \
                        isinstance(value, str):
                    value = datetime.strptime(value,
                                              "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, key, value)
            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.utcnow()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
            if not DB:
                import models
                models.storage.new(self)

        table = getattr(type(self), "__table__", None)
        if DB and table is not None:
            for col in table.columns:
                if col.name in self.__dict__:
                    continue
                if isinstance(col.type, Integer):
                    setattr(self, col.name, 0)
                elif isinstance(col.type, Float):
                    setattr(self, col.name, 0.0)

    def __str__(self):
        """String representation"""
        d = {k: v for k, v in self.__dict__.items()
             if k != "_sa_instance_state"}
        return "[{}] ({}) {}".format(type(self).__name__, self.id, d)

    def save(self):
        """Update updated_at and save to storage"""
        import models
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation"""
        d = dict(self.__dict__)
        d.pop("_sa_instance_state", None)
        d["__class__"] = type(self).__name__
        d["created_at"] = self.created_at.isoformat()
        d["updated_at"] = self.updated_at.isoformat()
        return d

    def delete(self):
        """Delete this instance from storage"""
        import models
        models.storage.delete(self)
