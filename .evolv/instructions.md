# Relational Design lab: a course enrollment schema

You design the database for a course coordinator: three PostgreSQL tables, `students`, `courses` and `enrollments`, that refuse bad data on their own.
You write them in one file, `src/main/sql/schema.sql`.
The tests load your file into a fresh database and try inserts and deletes that your tables must accept or reject.

**Time:** about 30 minutes for the tasks, plus up to 10 minutes the first time if your PostgreSQL connection needs the [setup](#setup) steps.

## Before you start: PostgreSQL

The tests need a PostgreSQL server they can reach (16 or later). See [Prerequisites](#prerequisites) for the connection check, and [Setup](#setup) if your server needs other connection settings or a password.
If no server is reachable, every test fails with `Could not reach PostgreSQL to create the lab database`. That is a missing prerequisite, not a mistake in your schema.

## Quick start

1. Open `src/main/sql/schema.sql`. It holds only comments.
2. Select **Run Tests** before you change anything.

   **All 5 tests fail at first. That is expected: the file holds no tables yet.**
   Each failure names the task, table, column or criterion to fix next.
3. Work through the checklist below. After each task, select **Run Tests** again and read the remaining failures.
4. **You are finished when all 5 tests pass.** Then select **Submit**.

```
OPEN schema.sql -> RUN TESTS: 5 fail (expected)
  -> READ the failures -> EDIT the next task -> RUN TESTS again
  -> repeat for Tasks 1-5 -> SUBMIT when all 5 tests pass
```

In words: open the file, run the tests, read which tasks fail, complete one task, run the tests again, and submit when they all pass.

## Checklist

All five tasks are in `src/main/sql/schema.sql`. Read [the user story](#the-user-story) first.

- [ ] Task 1: create the three tables (test `task1Tables`)
- [ ] Task 2: make `students` meet criterion 1 (test `task2Students`)
- [ ] Task 3: make `courses` meet criterion 2 (test `task3Courses`)
- [ ] Task 4: connect students and courses, criteria 3 and 5 (test `task4EnrollmentKeys`)
- [ ] Task 5: record when and how well, criterion 4 (test `task5EnrollmentDefaults`)

A task is done when its test passes.
Edit only `schema.sql`. The tests in `src/test/java/relational/` are restored to their original state before your work is graded, so changes to them do not count. Leave the build file `pom.xml` and `expected/test-summary.txt` as they are.

From a terminal in the project folder, you can run one task's test on its own, for example `mvn -q test -Dtest='SchemaTest#task1Tables'`, or all of them with `mvn -q test`.
`WARNING:` lines from Java or Maven, such as `WARNING: A restricted method ...`, are not test failures.

## The user story

> As a course coordinator, I want students to enroll in courses, so that I can see who takes each course and record their grades.

Acceptance criteria:

1. Each student has an id (a whole number), a name of at most 100 characters and an email address. Name and email are required, and no two students share an email.
2. Each course is identified by a code such as `SQL101`. It has a required title and a required capacity, a whole number greater than 0.
3. A student can enroll in many courses, and a course has many students. A student cannot enroll in the same course twice.
4. Each enrollment always records when it was made, as a date and time: when no time is given, the current time is filled in. It also has a grade: empty until graded, otherwise an exact number from 0 to 100 with at most two decimal places.
5. An enrollment must refer to an existing student and an existing course. A student who has enrollments cannot be deleted.

Use exactly these table and column names, because the tests look them up:

| Table | Columns |
| --- | --- |
| `students` | `id`, `name`, `email` |
| `courses` | `code`, `title`, `capacity` |
| `enrollments` | `student_id`, `course_code`, `enrolled_at`, `grade` |

You choose the data types, keys, constraints and defaults. Any design that meets the criteria passes; the tests check behaviour, not one way of writing it.

## Task steps

### Task 1: create the three tables

1. Below the comment lines of `schema.sql`, write one `CREATE TABLE` statement for each table, with every listed column.
2. Create `students` and `courses` before `enrollments`, because a foreign key can only point at a table that already exists.
3. Until all three tables and ten columns exist, the test says `schema.sql must create a table named ...` or `Table ... has no column named ...`.
4. If the file has an SQL mistake, every test says `schema.sql did not run:` followed by PostgreSQL's message. Fix that first.

<details><summary>Hint</summary>

Pick a data type for each column now; you can refine types and add constraints in the next tasks.

</details>

### Task 2: make `students` meet criterion 1

A failure starts with `Criterion 1 (students):` and names the missing rule.

<details><summary>Hint</summary>

For each column, decide which data type fits its values and which rules PostgreSQL must enforce: which column identifies a student, which values are required, which must be unique, and how a name longer than 100 characters is refused.

</details>

### Task 3: make `courses` meet criterion 2

A failure starts with `Criterion 2 (courses):`.

<details><summary>Hint</summary>

Decide which column identifies a course and what type suits a code like `SQL101`, which columns are required, and how to refuse a capacity that is not greater than 0.

</details>

### Task 4: connect students and courses (criteria 3 and 5)

Work in `enrollments`. A failure starts with `Criterion 3 (many-to-many):` or `Criterion 5 (existing student and course):`.

<details><summary>Hint</summary>

Decide which columns must refer to which table, which of them are required, and which combination of columns must be unique so a student cannot enroll in the same course twice. Use column types that match the columns they refer to.

</details>

### Task 5: record when and how well (criterion 4)

Work on the `enrolled_at` and `grade` columns. A failure starts with `Criterion 4 (enrollment time and grade):`.

<details><summary>Hint</summary>

For `enrolled_at`, choose a type that holds a date and a time of day, make it required, and give it a default so PostgreSQL fills in the current time. For `grade`, choose an exact decimal type that keeps two decimal places, allow it to be empty, and refuse values outside 0 to 100.

</details>

**Starting over:** delete every line of `schema.sql` below its comment block. The shipped file holds only comments, so all five tests fail again.

## What the tests do

Each run creates a new database with a unique name such as `relational_design_lab_3f9c0a1b7d2e`, runs your `schema.sql` in it, runs the tests, and drops that database.
It never touches a database it did not create. While a run is in progress, the database's name is in `target/lab-database.txt`.
The tests talk only to that PostgreSQL server.

## Using an AI assistant

If you use an AI assistant, ask it to explain, not to answer.
"Explain what a composite primary key does" teaches you design; "write my schema" does not.
Check any explanation with a test run before you trust it.

## Prerequisites

| Tool | Version | Check |
| --- | --- | --- |
| PostgreSQL server and `psql` | 16 or later | the connection check below |
| JDK (only for terminal runs) | 17 or later | `java -version` |
| Apache Maven (only for terminal runs) | 3.9 or later | `mvn -v` |

### Connection check

The tests connect to `localhost` port `5432` as your login user, through database `postgres`. Check that the same connection works:

```
psql -h localhost -p 5432 -d postgres -c "SELECT version();"
```

It should print one row starting `PostgreSQL 16` (or later) without asking for a password.

## Setup

Only if the connection check needs other values: the tests read the same environment variables as `psql`.

| Variable | Meaning | Default |
| --- | --- | --- |
| `PGHOST` | server host name (not a socket folder) | `localhost` |
| `PGPORT` | server port | `5432` |
| `PGUSER` | a PostgreSQL user allowed to create databases | your login name |
| `PGDATABASE` | an existing database to connect to first | `postgres` |

For a terminal run, set the ones you need in that terminal, for example `export PGUSER=postgres` (macOS or Linux) or `$env:PGUSER = "postgres"` (Windows PowerShell). They last until you close it.

**If your server asks for a password**, put it in a password file, which both `psql` and the tests read. Write one line, `localhost:5432:*:postgres:your-password`, with your own port, user and password:

- macOS or Linux: in `~/.pgpass`, then run `chmod 600 ~/.pgpass` (`psql` ignores a password file that others can read).
- Windows: in `%APPDATA%\postgresql\pgpass.conf` (create the `postgresql` folder if it is missing).

Never write a password into `schema.sql` or any file you share. The tests also accept a `PGPASSWORD` variable, but PostgreSQL recommends against it, because on some systems other users can read it.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| `Could not reach PostgreSQL to create the lab database`, `Connection refused` or `could not connect` | Run the [connection check](#connection-check). If it fails too, start your PostgreSQL server or check its port. |
| `password authentication failed` or `no password was provided` | Set up a [password file](#setup), or set `PGUSER`. |
| `role "..." does not exist` | Your login name is not a PostgreSQL user. Set `PGUSER` to one that is, such as `postgres` (see [Setup](#setup)). |
| `permission denied to create database` | Use a PostgreSQL user that may create databases, such as `postgres`. |
| `PGHOST is set to "...", which is not a host name` | The tests connect over TCP. Set `PGHOST` to `localhost` or your server's host name. |
| `schema.sql did not run: ... relation "students" does not exist` | A foreign key points at a table created later in the file. Create `students` and `courses` first. |
| A run was interrupted | Drop the database named in `target/lab-database.txt`, for example `psql -h localhost -d postgres -c "DROP DATABASE relational_design_lab_3f9c0a1b7d2e;"` with the name from the file. |
