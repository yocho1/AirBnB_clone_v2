#!/usr/bin/python3
"""Unit tests for Place class"""

import os
import unittest
from models.place import Place


class TestPlace(unittest.TestCase):
    """Test cases for Place class"""

    def test_inheritance(self):
        """Test Place inherits from BaseModel"""
        place = Place()
        self.assertTrue(hasattr(place, 'id'))
        self.assertTrue(hasattr(place, 'created_at'))
        self.assertTrue(hasattr(place, 'updated_at'))

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "FileStorage only")
    def test_attributes(self):
        """Test Place attributes exist"""
        place = Place()
        self.assertEqual(place.city_id, "")
        self.assertEqual(place.user_id, "")
        self.assertEqual(place.name, "")
        self.assertEqual(place.description, "")
        self.assertEqual(place.number_rooms, 0)
        self.assertEqual(place.number_bathrooms, 0)
        self.assertEqual(place.max_guest, 0)
        self.assertEqual(place.price_by_night, 0)
        self.assertEqual(place.latitude, 0.0)
        self.assertEqual(place.longitude, 0.0)
        self.assertEqual(place.amenity_ids, [])
