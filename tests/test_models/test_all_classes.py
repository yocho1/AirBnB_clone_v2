#!/usr/bin/python3
"""Deeper round-trip tests for all AirBnB model classes."""
import os
import unittest
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

FMT = "%Y-%m-%dT%H:%M:%S.%f"
CLASSES = {
    "BaseModel": BaseModel,
    "User": User,
    "State": State,
    "City": City,
    "Amenity": Amenity,
    "Place": Place,
    "Review": Review,
}


DB_MODE = os.getenv("HBNB_TYPE_STORAGE") == "db"


class TestAllClassesSerialization(unittest.TestCase):
    """Verify to_dict, reconstruction, and save work for every class."""

    def setUp(self):
        """Reset storage in-memory dictionary and delete test file."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        storage.all().clear()

    def tearDown(self):
        """Clean up generated JSON file after tests run."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_to_dict_class_key_matches(self):
        """__class__ in to_dict() matches the real class name."""
        for cls_name, cls in CLASSES.items():
            with self.subTest(cls_name=cls_name):
                obj = cls()
                d = obj.to_dict()
                self.assertEqual(d["__class__"], cls_name)

    def test_to_dict_datetimes_are_strings(self):
        """created_at/updated_at in to_dict() are ISO strings."""
        for cls_name, cls in CLASSES.items():
            with self.subTest(cls_name=cls_name):
                obj = cls()
                d = obj.to_dict()
                self.assertIsInstance(d["created_at"], str)
                self.assertIsInstance(d["updated_at"], str)
                parsed_created = datetime.strptime(d["created_at"], FMT)
                parsed_updated = datetime.strptime(d["updated_at"], FMT)
                self.assertIsInstance(parsed_created, datetime)
                self.assertIsInstance(parsed_updated, datetime)

    def test_reconstruction_round_trip(self):
        """Rebuilding via cls(**d) preserves id and datetimes."""
        for cls_name, cls in CLASSES.items():
            with self.subTest(cls_name=cls_name):
                original_obj = cls()
                dictionary = original_obj.to_dict()
                new_obj = cls(**dictionary)
                self.assertEqual(new_obj.id, original_obj.id)
                self.assertIsInstance(new_obj.created_at, datetime)
                self.assertIsInstance(new_obj.updated_at, datetime)
                self.assertEqual(
                    new_obj.created_at, original_obj.created_at
                )
                self.assertEqual(
                    new_obj.updated_at, original_obj.updated_at
                )
                self.assertEqual(new_obj.__class__.__name__, cls_name)

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_save_persists_to_storage(self):
        """save() updates updated_at and persists the storage key."""
        for cls_name, cls in CLASSES.items():
            with self.subTest(cls_name=cls_name):
                obj = cls()
                key = "{}.{}".format(cls_name, obj.id)
                self.assertIn(key, storage.all())
                old_updated_at = obj.updated_at
                obj.save()
                self.assertNotEqual(obj.updated_at, old_updated_at)
                storage.reload()
                self.assertIn(key, storage.all())
                self.assertEqual(storage.all()[key].id, obj.id)


if __name__ == "__main__":
    unittest.main()
