#!/usr/bin/python3
"""DBStorage: create User through the console, checked with MySQLdb."""
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


def count():
    """Number of rows in users."""
    return query("SELECT COUNT(*) FROM users")[0][0]


def run(cmd):
    """Run a console command and return its output."""
    with patch('sys.stdout', new=StringIO()) as output:
        HBNBCommand().onecmd(cmd)
    return output.getvalue().strip()


@unittest.skipUnless(DB_MODE, "DBStorage only")
class TestCreateUserDB(unittest.TestCase):
    """create User through the console, verified in MySQL."""

    def test_create_user_all_fields(self):
        """All four parameters are stored."""
        before = count()
        user_id = run('create User email="a@a.com" password="pwd" '
                      'first_name="fn" last_name="ln"')
        self.assertEqual(count() - before, 1)
        row = query("SELECT email, password, first_name, last_name "
                    "FROM users WHERE id=%s", (user_id,))[0]
        self.assertEqual(row, ("a@a.com", "pwd", "fn", "ln"))

    def test_create_user_email_password(self):
        """first_name and last_name are NULL when not given."""
        before = count()
        user_id = run('create User email="a@a.com" password="my_pwd"')
        self.assertEqual(count() - before, 1)
        row = query("SELECT email, password, first_name, last_name "
                    "FROM users WHERE id=%s", (user_id,))[0]
        self.assertEqual(row, ("a@a.com", "my pwd", None, None))

    def test_create_user_only_email(self):
        """No row without a password."""
        before = count()
        run('create User email="a@a.com"')
        self.assertEqual(count(), before)

    def test_create_user_only_password(self):
        """No row without an email."""
        before = count()
        run('create User password="pwd"')
        self.assertEqual(count(), before)

    def test_create_user_no_params(self):
        """No row without any parameter."""
        before = count()
        run("create User")
        self.assertEqual(count(), before)
