#!/usr/bin/python3
"""Unit tests for City class"""

import os
import unittest
from models.city import City


class TestCity(unittest.TestCase):
    """Test cases for City class"""

    def test_inheritance(self):
        """Test City inherits from BaseModel"""
        city = City()
        self.assertTrue(hasattr(city, 'id'))
        self.assertTrue(hasattr(city, 'created_at'))
        self.assertTrue(hasattr(city, 'updated_at'))

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "FileStorage only")
    def test_attributes(self):
        """Test City attributes exist"""
        city = City()
        self.assertEqual(city.state_id, "")
        self.assertEqual(city.name, "")

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "FileStorage only")
    def test_attribute_types(self):
        """Test City attribute types"""
        city = City()
        self.assertIsInstance(city.state_id, str)
        self.assertIsInstance(city.name, str)
