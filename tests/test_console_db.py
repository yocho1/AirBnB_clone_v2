#!/usr/bin/python3
"""DBStorage console tests, checked directly with MySQLdb."""
import os
import unittest
from io import StringIO
from unittest.mock import patch

DB_MODE = os.getenv("HBNB_TYPE_STORAGE") == "db"

if DB_MODE:
    import MySQLdb
    from console import HBNBCommand


def count_rows(table):
    """Count rows in a table using a fresh MySQLdb connection."""
    conn = MySQLdb.connect(host=os.getenv("HBNB_MYSQL_HOST"),
                           user=os.getenv("HBNB_MYSQL_USER"),
                           passwd=os.getenv("HBNB_MYSQL_PWD"),
                           db=os.getenv("HBNB_MYSQL_DB"))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM {}".format(table))
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total


@unittest.skipUnless(DB_MODE, "DBStorage only")
class TestConsoleDB(unittest.TestCase):
    """Console commands must change the MySQL tables."""

    def test_create_state_adds_row(self):
        """create State adds exactly one row to states."""
        before = count_rows("states")
        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd('create State name="California"')
        self.assertEqual(count_rows("states") - before, 1)

    def test_create_two_states_adds_two_rows(self):
        """Two creates add two rows."""
        before = count_rows("states")
        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd('create State name="Nevada"')
            HBNBCommand().onecmd('create State name="Texas"')
        self.assertEqual(count_rows("states") - before, 2)

    def test_create_user_adds_row(self):
        """create User adds exactly one row to users."""
        before = count_rows("users")
        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd(
                'create User email="a@b.com" password="pwd"')
        self.assertEqual(count_rows("users") - before, 1)

    def test_create_invalid_class_adds_nothing(self):
        """An invalid class leaves states unchanged."""
        before = count_rows("states")
        with patch('sys.stdout', new=StringIO()):
            HBNBCommand().onecmd('create Fake name="x"')
        self.assertEqual(count_rows("states"), before)
