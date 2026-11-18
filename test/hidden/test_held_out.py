"""Held-out tests: graded on submit, never shown to the learner.

They try the edge cases of each acceptance criterion against the learner's src/schema.sql.
"""

import psycopg

from test.support import accepted, rejected, seed, stored_grade


def test_task2_name_length(schema):
    db = schema
    c1 = "Criterion 1 (students):"
    seed(db)
    rejected(db, "INSERT INTO students (id, name, email) OVERRIDING SYSTEM VALUE VALUES (2, repeat('x', 101), 'ben@example.com')",
             {"22001", "23514"}, f"{c1} a name has at most 100 characters, so a 101-character name must be rejected.")
    accepted(db, "INSERT INTO students (id, name, email) OVERRIDING SYSTEM VALUE VALUES "
                 "(2, repeat('x', 100), 'a.very.long.address.for.a.student.with.many.parts@university.example.com')",
             f"{c1} a 100-character name and a long email address are allowed.")


def test_task3_capacity_edges(schema):
    db = schema
    c2 = "Criterion 2 (courses):"
    seed(db)
    rejected(db, "INSERT INTO courses (code, title, capacity) VALUES ('JDBC201', 'JDBC', -5)", "23514",
             f"{c2} capacity must be greater than 0, so -5 must be rejected.")
    accepted(db, "INSERT INTO courses (code, title, capacity) VALUES ('JDBC201', 'JDBC', 1)", f"{c2} a capacity of 1 is allowed.")


def test_task4_deleting_students(schema):
    db = schema
    c3 = "Criterion 3 (many-to-many):"
    c5 = "Criterion 5 (existing student and course):"
    seed(db)
    accepted(db, "INSERT INTO enrollments (student_id, course_code) VALUES (1, 'SQL101')", f"{c3} a student enrolls in a course.")
    rejected(db, "DELETE FROM students WHERE id = 1", {"23503", "23001"},
             f"{c5} a student who has enrollments cannot be deleted.")
    accepted(db, "INSERT INTO students (id, name, email) OVERRIDING SYSTEM VALUE VALUES (3, 'Chen Wei', 'chen@example.com')",
             f"{c5} a student with no enrollments.")
    accepted(db, "DELETE FROM students WHERE id = 3", f"{c5} a student with no enrollments can be deleted.")


def test_task5_grade_edges(schema):
    db = schema
    c4 = "Criterion 4 (enrollment time and grade):"
    seed(db)
    accepted(db, "INSERT INTO courses (code, title, capacity) VALUES ('WEB101', 'Web', 20)", f"{c4} a second course.")
    rejected(db, "INSERT INTO enrollments (student_id, course_code, grade) VALUES (1, 'WEB101', -1)", "23514",
             f"{c4} a grade is at least 0.")
    accepted(db, "INSERT INTO enrollments (student_id, course_code, grade) VALUES (1, 'WEB101', 100)", f"{c4} a grade of 100 is allowed.")
    accepted(db, "DELETE FROM enrollments WHERE course_code = 'WEB101'", f"{c4} an enrollment can be removed.")
    try:
        with db.transaction():
            db.execute("INSERT INTO enrollments (student_id, course_code, grade) VALUES (1, 'WEB101', 87.255)")
            stored = stored_grade(db, "WEB101")
            assert stored.normalize().as_tuple().exponent >= -2, \
                f"{c4} a grade keeps at most two decimal places, but 87.255 was stored as {format(stored, 'f')}."
    except psycopg.Error:
        pass  # rejecting a third decimal place also meets the criterion
