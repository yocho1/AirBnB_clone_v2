#!/usr/bin/python3
"""Unit tests for FileStorage class"""

import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models import storage


class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage class"""

    def setUp(self):
        """Set up test environment"""
        self.storage = FileStorage()
        self.test_file = "file.json"
        # Remove test file if exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_all(self):
        """Test all() method returns dictionary"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new(self):
        """Test new() method adds object"""
        obj = BaseModel()
        self.storage.new(obj)
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertIn(key, self.storage.all())

    def test_save(self):
        """Test save() method creates file"""
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        self.assertTrue(os.path.exists(self.test_file))
        # Check file has content
        with open(self.test_file, 'r') as f:
            content = json.load(f)
            self.assertIsInstance(content, dict)

    def test_reload(self):
        """Test reload() method loads objects"""
        obj = BaseModel()
        obj.name = "Test"
        self.storage.new(obj)
        self.storage.save()

        # Create new storage instance and reload
        new_storage = FileStorage()
        new_storage.reload()
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.assertIn(key, new_storage.all())
        reloaded_obj = new_storage.all()[key]
        self.assertEqual(reloaded_obj.name, "Test")

    def test_reload_no_file(self):
        """Test reload() with no file does nothing"""
        # Ensure file doesn't exist
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.storage.reload()  # Should not raise exception
        self.assertEqual(len(self.storage.all()), 0)


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                 "FileStorage only")
class TestFileStorageDelete(unittest.TestCase):
    """Tests for delete() and all(cls)"""

    def setUp(self):
        """Empty storage"""
        storage.all().clear()

    def tearDown(self):
        """Empty storage and remove the file"""
        storage.all().clear()
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_delete_removes_object(self):
        """delete() removes obj from __objects"""
        state = State()
        storage.new(state)
        storage.delete(state)
        self.assertNotIn("State.{}".format(state.id), storage.all())

    def test_delete_none_does_nothing(self):
        """delete(None) changes nothing"""
        state = State()
        storage.new(state)
        storage.delete(None)
        self.assertEqual(len(storage.all()), 1)

    def test_delete_missing_object(self):
        """delete() of an unknown object does not fail"""
        storage.delete(State())
        self.assertEqual(len(storage.all()), 0)

    def test_all_filters_by_class(self):
        """all(cls) returns only that class"""
        state = State()
        city = City()
        storage.new(state)
        storage.new(city)
        self.assertEqual(list(storage.all(State).values()), [state])
        self.assertEqual(len(storage.all()), 2)
