#!/usr/bin/python3
"""Unit tests for the HBNB console."""
import os
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage

DB_MODE = os.getenv("HBNB_TYPE_STORAGE") == "db"
CLASSES = ["BaseModel", "User", "State", "City",
           "Amenity", "Place", "Review"]


class TestHBNBCommand_create(unittest.TestCase):
    """Tests for the create command in HBNBCommand."""

    def setUp(self):
        """Reset storage and clear JSON file before each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        storage.all().clear()

    def tearDown(self):
        """Clean up JSON file after tests."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_create_missing_class(self):
        """Test output when no class name is given."""
        expected = "** class name missing **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("create")
        self.assertEqual(output.getvalue().strip(), expected)

    def test_create_invalid_class(self):
        """Test output when an invalid class name is given."""
        expected = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("create FakeClass")
        self.assertEqual(output.getvalue().strip(), expected)

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_create_valid_class(self):
        """Test output and storage side effects for a valid create."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("create BaseModel")
        generated_id = output.getvalue().strip()
        self.assertEqual(len(generated_id), 36)
        key = "BaseModel.{}".format(generated_id)
        self.assertIn(key, storage.all())

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_create_all_classes(self):
        """Test creating instances for all supported AirBnB models."""
        for cls_name in CLASSES:
            with self.subTest(cls_name=cls_name):
                with patch('sys.stdout', new=StringIO()) as output:
                    HBNBCommand().onecmd("create {}".format(cls_name))
                generated_id = output.getvalue().strip()
                self.assertEqual(len(generated_id), 36)
                key = "{}.{}".format(cls_name, generated_id)
                self.assertIn(key, storage.all())
                obj = storage.all()[key]
                self.assertEqual(obj.__class__.__name__, cls_name)


class TestHBNBCommand_show(unittest.TestCase):
    """Tests for the show command in HBNBCommand."""

    def setUp(self):
        """Reset storage and clear JSON file before each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        storage.all().clear()

    def tearDown(self):
        """Clean up JSON file after tests."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_show_missing_class(self):
        """Test output when no class name is provided."""
        expected = "** class name missing **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("show")
        self.assertEqual(output.getvalue().strip(), expected)

    def test_show_invalid_class(self):
        """Test output when an invalid class name is provided."""
        expected = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("show FakeClass 123")
        self.assertEqual(output.getvalue().strip(), expected)

    def test_show_missing_id(self):
        """Test output when instance id is missing."""
        expected = "** instance id missing **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("show BaseModel")
        self.assertEqual(output.getvalue().strip(), expected)

    def test_show_no_instance_found(self):
        """Test output when the instance id does not exist."""
        expected = "** no instance found **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("show BaseModel fake-id-123")
        self.assertEqual(output.getvalue().strip(), expected)

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_show_valid(self):
        """Test showing a valid existing instance."""
        with patch('sys.stdout', new=StringIO()) as create_out:
            HBNBCommand().onecmd("create BaseModel")
        obj_id = create_out.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as show_out:
            HBNBCommand().onecmd("show BaseModel {}".format(obj_id))

        out_str = show_out.getvalue().strip()
        expected_prefix = "[BaseModel] ({})".format(obj_id)
        self.assertTrue(out_str.startswith(expected_prefix))

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_show_all_classes(self):
        """Test showing a valid instance for every supported class."""
        for cls_name in CLASSES:
            with self.subTest(cls_name=cls_name):
                with patch('sys.stdout', new=StringIO()) as create_out:
                    HBNBCommand().onecmd("create {}".format(cls_name))
                obj_id = create_out.getvalue().strip()

                with patch('sys.stdout', new=StringIO()) as show_out:
                    cmd = "show {} {}".format(cls_name, obj_id)
                    HBNBCommand().onecmd(cmd)

                out_str = show_out.getvalue().strip()
                expected_prefix = "[{}] ({})".format(cls_name, obj_id)
                self.assertTrue(out_str.startswith(expected_prefix))


class TestHBNBCommand_destroy(unittest.TestCase):
    """Tests for the destroy command in HBNBCommand."""

    def setUp(self):
        """Reset storage and clear JSON file before each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        storage.all().clear()

    def tearDown(self):
        """Clean up JSON file after tests."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_destroy_missing_class(self):
        """Test output when no class name is provided."""
        expected = "** class name missing **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("destroy")
        self.assertEqual(output.getvalue().strip(), expected)

    def test_destroy_invalid_class(self):
        """Test output when an invalid class name is provided."""
        expected = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("destroy FakeClass 123")
        self.assertEqual(output.getvalue().strip(), expected)

    def test_destroy_missing_id(self):
        """Test output when instance id is missing."""
        expected = "** instance id missing **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("destroy BaseModel")
        self.assertEqual(output.getvalue().strip(), expected)

    def test_destroy_no_instance_found(self):
        """Test output when the instance id does not exist."""
        expected = "** no instance found **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("destroy BaseModel fake-id-123")
        self.assertEqual(output.getvalue().strip(), expected)

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_destroy_valid(self):
        """Test destroying an instance removes it from storage."""
        with patch('sys.stdout', new=StringIO()) as create_out:
            HBNBCommand().onecmd("create BaseModel")
        obj_id = create_out.getvalue().strip()
        key = "BaseModel.{}".format(obj_id)
        self.assertIn(key, storage.all())

        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd("destroy BaseModel {}".format(obj_id))

        self.assertNotIn(key, storage.all())

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_destroy_all_classes(self):
        """Test destroying a valid instance for every supported class."""
        for cls_name in CLASSES:
            with self.subTest(cls_name=cls_name):
                with patch('sys.stdout', new=StringIO()) as create_out:
                    HBNBCommand().onecmd("create {}".format(cls_name))
                obj_id = create_out.getvalue().strip()
                key = "{}.{}".format(cls_name, obj_id)
                self.assertIn(key, storage.all())

                with patch('sys.stdout', new=StringIO()):
                    cmd = "destroy {} {}".format(cls_name, obj_id)
                    HBNBCommand().onecmd(cmd)

                self.assertNotIn(key, storage.all())


class TestHBNBCommand_all(unittest.TestCase):
    """Tests for the all command in HBNBCommand."""

    def setUp(self):
        """Reset storage and clear JSON file before each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        storage.all().clear()

    def tearDown(self):
        """Clean up JSON file after tests."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all_invalid_class(self):
        """Test output when an invalid class name is provided."""
        expected = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("all FakeClass")
        self.assertEqual(output.getvalue().strip(), expected)

    def test_all_empty(self):
        """Test output when storage is empty."""
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("all")
        self.assertEqual(output.getvalue().strip(), "[]")

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_all_with_objects(self):
        """Test all command output with existing instances."""
        with patch('sys.stdout', new=StringIO()) as create1:
            HBNBCommand().onecmd("create BaseModel")
        id1 = create1.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as create2:
            HBNBCommand().onecmd("create BaseModel")
        id2 = create2.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as output_all:
            HBNBCommand().onecmd("all")
        out_str = output_all.getvalue().strip()
        self.assertIn(id1, out_str)
        self.assertIn(id2, out_str)

        with patch('sys.stdout', new=StringIO()) as output_bm:
            HBNBCommand().onecmd("all BaseModel")
        out_bm_str = output_bm.getvalue().strip()
        self.assertIn(id1, out_bm_str)
        self.assertIn(id2, out_bm_str)

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_all_filters_by_class(self):
        """Test that 'all <class>' only returns that class's objects."""
        with patch('sys.stdout', new=StringIO()) as create_state:
            HBNBCommand().onecmd("create State")
        state_id = create_state.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as create_city:
            HBNBCommand().onecmd("create City")
        city_id = create_city.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("all State")
        out_str = output.getvalue().strip()
        self.assertIn(state_id, out_str)
        self.assertNotIn(city_id, out_str)


class TestHBNBCommand_update(unittest.TestCase):
    """Tests for the update command in HBNBCommand."""

    def setUp(self):
        """Reset storage and clear JSON file before each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        storage.all().clear()

    def tearDown(self):
        """Clean up JSON file after tests."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_update_missing_class(self):
        """Test output when no class name is provided."""
        expected = "** class name missing **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("update")
        self.assertEqual(output.getvalue().strip(), expected)

    def test_update_invalid_class(self):
        """Test output when an invalid class name is provided."""
        expected = "** class doesn't exist **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("update FakeClass 123")
        self.assertEqual(output.getvalue().strip(), expected)

    def test_update_missing_id(self):
        """Test output when instance id is missing."""
        expected = "** instance id missing **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("update BaseModel")
        self.assertEqual(output.getvalue().strip(), expected)

    def test_update_no_instance_found(self):
        """Test output when the instance id does not exist."""
        expected = "** no instance found **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("update BaseModel fake-id-123")
        self.assertEqual(output.getvalue().strip(), expected)

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_update_missing_attr_name(self):
        """Test output when attribute name is missing."""
        with patch('sys.stdout', new=StringIO()) as create_out:
            HBNBCommand().onecmd("create BaseModel")
        obj_id = create_out.getvalue().strip()

        expected = "** attribute name missing **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("update BaseModel {}".format(obj_id))
        self.assertEqual(output.getvalue().strip(), expected)

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_update_missing_attr_value(self):
        """Test output when attribute value is missing."""
        with patch('sys.stdout', new=StringIO()) as create_out:
            HBNBCommand().onecmd("create BaseModel")
        obj_id = create_out.getvalue().strip()

        expected = "** value missing **"
        with patch('sys.stdout', new=StringIO()) as output:
            HBNBCommand().onecmd("update BaseModel {} name".format(obj_id))
        self.assertEqual(output.getvalue().strip(), expected)

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_update_valid(self):
        """Test updating an instance attribute dynamically."""
        with patch('sys.stdout', new=StringIO()) as create_out:
            HBNBCommand().onecmd("create BaseModel")
        obj_id = create_out.getvalue().strip()

        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd(
                'update BaseModel {} name "New Name"'.format(obj_id)
            )

        key = "BaseModel.{}".format(obj_id)
        obj = storage.all()[key]
        self.assertTrue(hasattr(obj, "name"))
        self.assertEqual(obj.name, "New Name")

    @unittest.skipIf(DB_MODE, "FileStorage only")
    def test_update_all_classes(self):
        """Test updating an attribute for every supported class."""
        for cls_name in CLASSES:
            with self.subTest(cls_name=cls_name):
                with patch('sys.stdout', new=StringIO()) as create_out:
                    HBNBCommand().onecmd("create {}".format(cls_name))
                obj_id = create_out.getvalue().strip()

                with patch('sys.stdout', new=StringIO()):
                    cmd = 'update {} {} name "Test Name"'.format(
                        cls_name, obj_id
                    )
                    HBNBCommand().onecmd(cmd)

                key = "{}.{}".format(cls_name, obj_id)
                obj = storage.all()[key]
                self.assertEqual(obj.name, "Test Name")


if __name__ == "__main__":
    unittest.main()
