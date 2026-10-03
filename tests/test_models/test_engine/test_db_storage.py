#!/usr/bin/python3
"""Unit tests for DBStorage class"""

import unittest
import os
from models.engine.db_storage import DBStorage


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "DBStorage tests only run for DB storage")
class TestDBStorage(unittest.TestCase):
    """Test cases for DBStorage class"""

    def setUp(self):
        """Set up test environment"""
        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """Clean up after tests"""
        self.storage.close()

    def test_all(self):
        """Test all() returns dict"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new(self):
        """Test new() adds an object"""
        from models.state import State
        state = State(name="California")
        self.storage.new(state)
        self.storage.save()
        all_objs = self.storage.all()
        key = "State.{}".format(state.id)
        self.assertIn(key, all_objs)

    def test_save(self):
        """Test save() persists data"""
        from models.state import State
        state = State(name="TestState")
        self.storage.new(state)
        self.storage.save()
        # Verify by reloading
        self.storage.reload()
        key = "State.{}".format(state.id)
        self.assertIn(key, self.storage.all())

    def test_delete(self):
        """Test delete() removes an object"""
        from models.state import State
        state = State(name="ToDelete")
        self.storage.new(state)
        self.storage.save()
        key = "State.{}".format(state.id)
        self.assertIn(key, self.storage.all())
        self.storage.delete(state)
        self.storage.save()
        self.assertNotIn(key, self.storage.all())

    def test_all_with_class(self):
        """Test all() with class filter"""
        from models.state import State
        state = State(name="Filtered")
        self.storage.new(state)
        self.storage.save()
        states = self.storage.all(State)
        key = "State.{}".format(state.id)
        self.assertIn(key, states)
