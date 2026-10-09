#!/usr/bin/python3
"""DBStorage: create State and City with parameters, checked in MySQL."""
import os
import unittest
from io import StringIO
from unittest.mock import patch

DB_MODE = os.getenv("HBNB_TYPE_STORAGE") == "db"

if DB_MODE:
    import MySQLdb
    from console import HBNBCommand


def query(sql, args=()):
    """Run a SELECT with a fresh MySQLdb connection."""
    conn = MySQLdb.connect(host=os.getenv("HBNB_MYSQL_HOST"),
                           user=os.getenv("HBNB_MYSQL_USER"),
                           passwd=os.getenv("HBNB_MYSQL_PWD"),
                           db=os.getenv("HBNB_MYSQL_DB"))
    cur = conn.cursor()
    cur.execute(sql, args)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def count(table):
    """Number of rows in a table."""
    return query("SELECT COUNT(*) FROM " + table)[0][0]


def run(cmd):
    """Run a console command and return its output."""
    with patch('sys.stdout', new=StringIO()) as output:
        HBNBCommand().onecmd(cmd)
    return output.getvalue().strip()


@unittest.skipUnless(DB_MODE, "DBStorage only")
class TestCreateStateCityDB(unittest.TestCase):
    """create State / City through the console, verified with MySQLdb."""

    def test_create_state_california(self):
        """create State name="California" adds one row with that name."""
        before = count("states")
        state_id = run('create State name="California"')
        self.assertEqual(count("states") - before, 1)
        rows = query("SELECT name FROM states WHERE id=%s", (state_id,))
        self.assertEqual(rows[0][0], "California")

    def test_create_state_then_city_fremont(self):
        """A State and a City with several parameters."""
        state_id = run('create State name="California"')
        before = count("cities")
        city_id = run('create City state_id="{}" name="Fremont"'
                      .format(state_id))
        self.assertEqual(count("cities") - before, 1)
        rows = query("SELECT name, state_id FROM cities WHERE id=%s",
                     (city_id,))
        self.assertEqual(rows[0], ("Fremont", state_id))

    def test_create_city_san_francisco_space(self):
        """Underscores in the value are stored as spaces."""
        state_id = run('create State name="California"')
        city_id = run('create City state_id="{}" name="San_Francisco"'
                      .format(state_id))
        rows = query("SELECT name FROM cities WHERE id=%s", (city_id,))
        self.assertEqual(rows[0][0], "San Francisco")

    def test_create_state_without_name_adds_nothing(self):
        """create State without name must not add a row."""
        before = count("states")
        run("create State")
        self.assertEqual(count("states"), before)

    def test_create_city_only_state_id_adds_nothing(self):
        """create City with only state_id must not add a row."""
        state_id = run('create State name="California"')
        before = count("cities")
        run('create City state_id="{}"'.format(state_id))
        self.assertEqual(count("cities"), before)

    def test_create_city_unknown_state_adds_nothing(self):
        """A state_id that does not exist must not add a row."""
        before = count("cities")
        run('create City state_id="no-such-id" name="Fremont"')
        self.assertEqual(count("cities"), before)

    def test_create_city_only_name_adds_nothing(self):
        """create City with only name must not add a row."""
        before = count("cities")
        run('create City name="Fremont"')
        self.assertEqual(count("cities"), before)
