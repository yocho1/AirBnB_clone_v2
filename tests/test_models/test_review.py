#!/usr/bin/python3
"""Unit tests for Review class"""

import os
import unittest
from models.review import Review


class TestReview(unittest.TestCase):
    """Test cases for Review class"""

    def test_inheritance(self):
        """Test Review inherits from BaseModel"""
        review = Review()
        self.assertTrue(hasattr(review, 'id'))
        self.assertTrue(hasattr(review, 'created_at'))
        self.assertTrue(hasattr(review, 'updated_at'))

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "FileStorage only")
    def test_attributes(self):
        """Test Review attributes exist"""
        review = Review()
        self.assertEqual(review.place_id, "")
        self.assertEqual(review.user_id, "")
        self.assertEqual(review.text, "")

    @unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db",
                     "FileStorage only")
    def test_attribute_types(self):
        """Test Review attribute types"""
        review = Review()
        self.assertIsInstance(review.place_id, str)
        self.assertIsInstance(review.user_id, str)
        self.assertIsInstance(review.text, str)
