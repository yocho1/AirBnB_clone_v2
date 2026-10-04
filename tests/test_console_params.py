#!/usr/bin/python3
"""Tests for create with parameters (FileStorage)."""
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand, parse_value
from models import storage

DB_MODE = os.getenv("HBNB_TYPE_STORAGE") == "db"


def run(cmd):
    """Run a console command and return its output."""
    with patch('sys.stdout', new=StringIO()) as output:
        HBNBCommand().onecmd(cmd)
    return output.getvalue().strip()


@unittest.skipIf(DB_MODE, "FileStorage only")
class TestCreateParams(unittest.TestCase):
    """create <Class> <key>=<value> ..."""

    def setUp(self):
        """Reset storage."""
        storage.all().clear()
        if os.path.exists("file.json"):
            os.remove("file.json")

    def tearDown(self):
        """Remove the JSON file."""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def get(self, cls_name, obj_id):
        """Return the stored object."""
        return storage.all()["{}.{}".format(cls_name, obj_id)]

    def test_string_underscores(self):
        """Underscores become spaces."""
        obj_id = run('create State name="My_little_house"')
        self.assertEqual(self.get("State", obj_id).name, "My little house")

    def test_string_escaped_quote(self):
        """Escaped double quotes are kept."""
        obj_id = run('create State name="Say_\\"hi\\""')
        self.assertEqual(self.get("State", obj_id).name, 'Say "hi"')

    def test_integer(self):
        """Integers are parsed."""
        obj_id = run('create Place number_rooms=4')
        place = self.get("Place", obj_id)
        self.assertEqual(place.number_rooms, 4)
        self.assertIsInstance(place.number_rooms, int)

    def test_float(self):
        """Floats are parsed."""
        obj_id = run('create Place latitude=37.77 longitude=-122.43')
        place = self.get("Place", obj_id)
        self.assertEqual(place.latitude, 37.77)
        self.assertEqual(place.longitude, -122.43)

    def test_invalid_params_skipped(self):
        """Invalid parameters are skipped, valid ones kept."""
        obj_id = run('create Place max_guest=abc name="ok" bad=1.2.3 '
                     'oops="no')
        place = self.get("Place", obj_id)
        self.assertEqual(place.name, "ok")
        self.assertEqual(place.max_guest, 0)
        self.assertFalse(hasattr(place, "bad"))
        self.assertFalse(hasattr(place, "oops"))

    def test_unescaped_quote_skipped(self):
        """An unescaped quote inside a string skips the parameter."""
        self.assertIsNone(parse_value('"a"b"'))

    def test_parse_value(self):
        """parse_value handles each type."""
        self.assertEqual(parse_value('"a_b"'), "a b")
        self.assertEqual(parse_value("3"), 3)
        self.assertEqual(parse_value("3.5"), 3.5)
        self.assertIsNone(parse_value("x"))

    def test_no_params(self):
        """create without parameters still works."""
        obj_id = run("create State")
        self.assertIn("State.{}".format(obj_id), storage.all())

    def test_missing_and_invalid_class(self):
        """Error messages are unchanged."""
        self.assertEqual(run("create"), "** class name missing **")
        self.assertEqual(run("create Fake name=\"x\""),
                         "** class doesn't exist **")

    def test_saved_to_file(self):
        """The object is written to file.json."""
        run('create State name="California"')
        with open("file.json") as f:
            self.assertIn("California", f.read())
