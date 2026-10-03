#!/usr/bin/python3
"""FileStorage class module"""

import json
import os


class FileStorage:
    """Serializes and deserializes objects to/from JSON"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return all objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Add object to storage"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Save all objects to JSON file"""
        serialized = {}
        for key, obj in FileStorage.__objects.items():
            serialized[key] = obj.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(serialized, f)

    def reload(self):
        """Load objects from JSON file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
            'BaseModel': BaseModel,
            'User': User,
            'Place': Place,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Review': Review
        }

        if not os.path.exists(FileStorage.__file_path):
            FileStorage.__objects = {}
            return

        try:
            with open(FileStorage.__file_path, 'r') as f:
                data = json.load(f)
                for key, dict_obj in data.items():
                    class_name = dict_obj.get('__class__')
                    cls = classes.get(class_name)
                    if cls:
                        obj = cls(**dict_obj)
                        FileStorage.__objects[key] = obj
        except (FileNotFoundError, json.JSONDecodeError):
            FileStorage.__objects = {}

    def delete(self, obj=None):
        """Delete an object from storage"""
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]
