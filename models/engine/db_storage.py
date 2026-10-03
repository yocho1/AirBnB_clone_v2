#!/usr/bin/python3
"""DBStorage class module"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    """Database storage engine using SQLAlchemy"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database engine"""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db),
            pool_pre_ping=True
        )

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Return all objects, or all objects of a specific class"""
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'User': User, 'Place': Place, 'State': State,
            'City': City, 'Amenity': Amenity, 'Review': Review
        }

        result = {}
        if cls is None:
            for class_name, class_obj in classes.items():
                objs = self.__session.query(class_obj).all()
                for obj in objs:
                    key = "{}.{}".format(class_name, obj.id)
                    result[key] = obj
        else:
            if isinstance(cls, str):
                cls = classes.get(cls)
            if cls:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = "{}.{}".format(cls.__name__, obj.id)
                    result[key] = obj
        return result

    def new(self, obj):
        """Add a new object to the session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create tables and session"""
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(session_factory)

    def close(self):
        """Close the session"""
        self.__session.remove()
