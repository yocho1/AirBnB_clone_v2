#!/usr/bin/python3
"""DBStorage: check the SQLAlchemy column definitions."""
import os
import unittest
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.place import Place

DB_MODE = os.getenv("HBNB_TYPE_STORAGE") == "db"


def fk_targets(col):
    """Return the 'table.column' targets of a column's foreign keys."""
    return [fk.target_fullname for fk in col.foreign_keys]


@unittest.skipUnless(DB_MODE, "DBStorage only")
class TestDBColumns(unittest.TestCase):
    """Columns have the types and constraints required by the project."""

    def test_state(self):
        """states.name is NOT NULL, 128 chars."""
        col = State.__table__.columns["name"]
        self.assertFalse(col.nullable)
        self.assertEqual(col.type.length, 128)

    def test_city(self):
        """cities has a NOT NULL name and a state_id foreign key."""
        cols = City.__table__.columns
        self.assertFalse(cols["name"].nullable)
        self.assertFalse(cols["state_id"].nullable)
        self.assertEqual(cols["state_id"].type.length, 60)
        self.assertEqual(fk_targets(cols["state_id"]), ["states.id"])

    def test_user(self):
        """users: email/password NOT NULL, names nullable."""
        cols = User.__table__.columns
        self.assertFalse(cols["email"].nullable)
        self.assertFalse(cols["password"].nullable)
        self.assertTrue(cols["first_name"].nullable)
        self.assertTrue(cols["last_name"].nullable)

    def test_amenity(self):
        """amenities.name is NOT NULL."""
        self.assertFalse(Amenity.__table__.columns["name"].nullable)

    def test_review(self):
        """reviews has foreign keys to places and users."""
        cols = Review.__table__.columns
        self.assertEqual(fk_targets(cols["place_id"]), ["places.id"])
        self.assertEqual(fk_targets(cols["user_id"]), ["users.id"])

    def test_place(self):
        """places has foreign keys to cities and users."""
        cols = Place.__table__.columns
        self.assertEqual(fk_targets(cols["city_id"]), ["cities.id"])
        self.assertEqual(fk_targets(cols["user_id"]), ["users.id"])

    def test_primary_key(self):
        """Every table has a 60-char string primary key id."""
        for cls in (State, City, User, Amenity, Review, Place):
            col = cls.__table__.columns["id"]
            self.assertTrue(col.primary_key)
            self.assertEqual(col.type.length, 60)
