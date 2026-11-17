"""Test plumbing shared by the visible tests and the held-out tests.

You need no PostgreSQL server of your own. The pgserver package (see requirements.txt) contains a
real PostgreSQL 16. The tests start a private copy of it in a temporary folder, give every test a
brand-new empty database, and delete the server and its data when the run ends. They never touch
any other database.
"""

from __future__ import annotations

import contextlib
import secrets
import tempfile
from decimal import Decimal
from pathlib import Path

import psycopg
import pytest

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

WHOLE_NUMBER = {"smallint", "integer", "bigint"}
CHARACTERS = {"text", "character varying"}


# ---------- the private PostgreSQL ----------

def start_server():
    """Starts a private PostgreSQL in a new temporary folder and returns its pgserver handle."""
    try:
        import pgserver
    except ImportError as error:
        raise RuntimeError(
            "The tests start their own PostgreSQL with the pgserver package, which is not installed. "
            "Run: python -m pip install -r requirements.txt (pgserver needs Python 3.9 to 3.12)."
        ) from error
    return pgserver.get_server(tempfile.mkdtemp(prefix="pglab-"), cleanup_mode="delete")


@contextlib.contextmanager
def fresh_database(server):
    """Creates a new, empty database, yields an autocommit connection to it, then drops it."""
    name = "lab_" + secrets.token_hex(6)
    with psycopg.connect(server.get_uri(), autocommit=True) as admin:
        admin.execute(f"CREATE DATABASE {name}")
        try:
            with psycopg.connect(server.get_uri(database=name), autocommit=True) as conn:
                yield conn
        finally:
            admin.execute(f"DROP DATABASE IF EXISTS {name} WITH (FORCE)")


# ---------- the learner's schema ----------

def load_schema(db) -> None:
    """Runs src/schema.sql in the test's database, or fails the test with PostgreSQL's message."""
    sql = (SRC / "schema.sql").read_text(encoding="utf-8")
    problem = None
    try:
        db.execute(sql)
    except psycopg.Error as error:
        problem = str(error).strip()
    if problem is not None:
        pytest.fail(f"schema.sql did not run: {problem}", pytrace=False)


def accepted(db, sql: str, criterion: str) -> None:
    """Runs a statement that the design must accept."""
    problem = None
    try:
        db.execute(sql)
    except psycopg.Error as error:
        problem = str(error).strip()
    if problem is not None:
        pytest.fail(f"{criterion}\n  This statement should be accepted, but PostgreSQL rejected it:\n  {sql}\n  {problem}",
                    pytrace=False)


def rejected(db, sql: str, sqlstates, criterion: str) -> None:
    """Runs a statement that must be rejected with one of the given SQLSTATEs (the kind of rule broken)."""
    states = {sqlstates} if isinstance(sqlstates, str) else set(sqlstates)
    state = problem = None
    try:
        with db.transaction():
            db.execute(sql)
    except psycopg.Error as error:
        state, problem = error.sqlstate, str(error).strip()
    if problem is None:
        pytest.fail(f"{criterion}\n  This statement should be rejected, but it was accepted:\n  {sql}", pytrace=False)
    if state not in states:
        pytest.fail(f"{criterion}\n  This statement should be rejected by a rule for that criterion, but the error was different:\n"
                    f"  {sql}\n  {problem}", pytrace=False)


def column_type(db, table: str, column: str) -> str:
    """The column's data_type from information_schema, for example integer, text or numeric."""
    row = db.execute(
        "SELECT data_type FROM information_schema.columns "
        "WHERE table_schema = 'public' AND table_name = %s AND column_name = %s", (table, column)).fetchone()
    if row is None:
        pytest.fail(f"Table {table} has no column named {column}. Use the names listed in the lab instructions.", pytrace=False)
    return row[0]


def stored_grade(db, course_code: str) -> Decimal:
    row = db.execute("SELECT grade FROM enrollments WHERE student_id = 1 AND course_code = %s", (course_code,)).fetchone()
    assert row is not None, "The enrollment just inserted should be there."
    return row[0]


def seed(db) -> None:
    accepted(db, "INSERT INTO students (id, name, email) OVERRIDING SYSTEM VALUE VALUES (1, 'Ana Lima', 'ana@example.com')",
             "Criterion 1: a valid student.")
    accepted(db, "INSERT INTO courses (code, title, capacity) VALUES ('SQL101', 'SQL Foundations', 30)",
             "Criterion 2: a valid course.")
