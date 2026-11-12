# Relational Design lab: a course enrollment schema

You design the database for a course coordinator: three PostgreSQL tables, `students`, `courses` and `enrollments`, that refuse bad data on their own. You write them in one file, `starter/schema.sql`. The tests load your file into a fresh database and try inserts and deletes that your tables must accept or reject.

```
OPEN the project -> EDIT a TODO -> RUN the tests -> READ the feedback -> STOP when all pass
                        ^                                  |
                        +------------ next task -----------+
```

In words: open the lab project, edit the TODO for one task, run the tests, read what the failing test tells you, and repeat with the next task. Stop when every test passes.

**Time:** about 30 minutes for the tasks, plus up to 10 minutes the first time if your workspace needs the [setup](#setup) steps.

## Quick start

1. **Open** the lab project in VS Code, then open its terminal with **Terminal > New Terminal**. Go into the Maven project folder:

   ```
   cd starter
   ```

   Run every command in this README from this `starter` folder.
2. **Run** the tests:

   ```
   mvn -q -o test
   ```

   **All 5 tests fail at first. That is expected:** the starter file holds only comments, and each failure is a task you have not done yet.

   If Maven instead says it cannot resolve a dependency, run `mvn -q dependency:go-offline` once (it needs the internet), then run the tests again.
3. **Edit** the file for one task in [Your tasks](#your-tasks).
4. **Read** the feedback: each failing test names the table, column or criterion to fix next. Run that task's test command again after each change.
5. **Stop** when the full run `mvn -q -o test` prints no `[ERROR]` lines.

The tests need a PostgreSQL server they can reach, JDK 25 and Maven 3.9 or later ([Prerequisites](#prerequisites)). If a command fails, see [Troubleshooting](#troubleshooting).

## Your tasks

All five tasks are in `starter/schema.sql`. Read [the user story](#the-user-story) first. After each task, run its test; it is done when the run prints no `[ERROR]` lines.

- [ ] **1. Create the three tables.**
  `mvn -q -o test -Dtest='SchemaTest#task1Tables'`
- [ ] **2. Make `students` meet criterion 1.**
  `mvn -q -o test -Dtest='SchemaTest#task2Students'`
- [ ] **3. Make `courses` meet criterion 2.**
  `mvn -q -o test -Dtest='SchemaTest#task3Courses'`
- [ ] **4. Connect students and courses (criteria 3 and 5).**
  `mvn -q -o test -Dtest='SchemaTest#task4EnrollmentKeys'`
- [ ] **5. Record when and how well (criterion 4).**
  `mvn -q -o test -Dtest='SchemaTest#task5EnrollmentDefaults'`

**Finish:** run all the tests with `mvn -q -o test`. You are done when it prints no `[ERROR]` lines and `target/surefire-reports/relational.SchemaTest.txt` begins with:

```
Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
```

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

## Task details

1. **Create the three tables.** Below the comment lines of `schema.sql`, write one `CREATE TABLE` statement for each table, with every listed column. Create `students` and `courses` before `enrollments`, because a foreign key can only point at a table that already exists.
   - Until all three tables and ten columns exist, the test says `schema.sql must create a table named ...` or `Table ... has no column named ...`.
   - If the file has an SQL mistake, every test says `schema.sql did not run:` followed by PostgreSQL's message. Fix that first.

   <details><summary>Hint</summary>

   Pick a data type for each column now; you can refine types and add constraints in the next tasks.

   </details>

2. **Make `students` meet criterion 1.** A failure starts with `Criterion 1 (students):` and names the missing rule.

   <details><summary>Hint</summary>

   For each column, decide which data type fits its values and which rules PostgreSQL must enforce: which column identifies a student, which values are required, which must be unique, and how a name longer than 100 characters is refused.

   </details>

3. **Make `courses` meet criterion 2.** A failure starts with `Criterion 2 (courses):`.

   <details><summary>Hint</summary>

   Decide which column identifies a course and what type suits a code like `SQL101`, which columns are required, and how to refuse a capacity that is not greater than 0.

   </details>

4. **Connect students and courses (criteria 3 and 5)** in `enrollments`. A failure starts with `Criterion 3 (many-to-many):` or `Criterion 5 (existing student and course):`.

   <details><summary>Hint</summary>

   Decide which columns must refer to which table, which of them are required, and which combination of columns must be unique so a student cannot enroll in the same course twice. Use column types that match the columns they refer to.

   </details>

5. **Record when and how well (criterion 4)** in the `enrolled_at` and `grade` columns. A failure starts with `Criterion 4 (enrollment time and grade):`.

   <details><summary>Hint</summary>

   For `enrolled_at`, choose a type that holds a date and a time of day, make it required, and give it a default so PostgreSQL fills in the current time. For `grade`, choose an exact decimal type that keeps two decimal places, allow it to be empty, and refuse values outside 0 to 100.

   </details>

**Starting over:** delete every line of `schema.sql` below its comment block. The shipped file holds only comments, so all five tests fail again.

## What the tests do

Each run creates a new database with a unique name such as `relational_design_lab_3f9c0a1b7d2e`, runs your `schema.sql` in it, runs the tests, and drops that database. It never touches a database it did not create. While a run is in progress, the database's name is in `starter/target/lab-database.txt`. After setup, the tests run offline and talk only to that PostgreSQL server.

## Prerequisites

| Tool | Version | Check |
| --- | --- | --- |
| PostgreSQL server and `psql` | 18 (16 or later works) | the connection check below |
| JDK | 25 | `java -version` |
| Apache Maven | 3.9 or later | `mvn -v` |

### Connection check

The tests connect to `localhost` port `5432` as your login user, through database `postgres`. Check that the same connection works:

```
psql -h localhost -p 5432 -d postgres -c "SELECT version();"
```

It should print one row starting `PostgreSQL 18` (or 16, 17) without asking for a password.

## Setup

The quick start is all the setup most learners need. Only if the connection check needs other values: the tests read the same environment variables as `psql`. Set the ones you need in the terminal where you run the tests; they last until you close it.

| Variable | Meaning | Default |
| --- | --- | --- |
| `PGHOST` | server host name (not a socket folder) | `localhost` |
| `PGPORT` | server port | `5432` |
| `PGUSER` | a PostgreSQL user allowed to create databases | your login name |
| `PGDATABASE` | an existing database to connect to first | `postgres` |

For example `export PGUSER=postgres` (macOS or Linux) or `$env:PGUSER = "postgres"` (Windows PowerShell).

**If your server asks for a password**, put it in a password file, which both `psql` and the tests read. Write one line, `localhost:5432:*:postgres:your-password`, with your own port, user and password:

- macOS or Linux: in `~/.pgpass`, then run `chmod 600 ~/.pgpass` (`psql` ignores a password file that others can read).
- Windows: in `%APPDATA%\postgresql\pgpass.conf` (create the `postgresql` folder if it is missing).

Never write a password into `schema.sql` or any file you share. The tests also accept a `PGPASSWORD` variable, but PostgreSQL recommends against it, because on some systems other users can read it.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| `cd: no such file or directory: starter` (or `Cannot find path`) | The terminal is not in the lab's top folder, the one that holds this `README.md` and the `starter` folder. Change to that folder, then run `cd starter`. |
| `Could not reach PostgreSQL to create the lab database`, `Connection refused` or `could not connect` | Run the [connection check](#connection-check). If it fails too, start your PostgreSQL server or check its port. |
| `password authentication failed` or `no password was provided` | Set up a [password file](#setup), or set `PGUSER`. |
| `role "..." does not exist` | Your login name is not a PostgreSQL user. Set `PGUSER` to one that is, such as `postgres` (see [Setup](#setup)). |
| `permission denied to create database` | Use a PostgreSQL user that may create databases, such as `postgres`. |
| `PGHOST is set to "...", which is not a host name` | The tests connect over TCP. Set `PGHOST` to `localhost` or your server's host name. |
| `schema.sql did not run: ... relation "students" does not exist` | A foreign key points at a table created later in the file. Create `students` and `courses` first. |
| Maven cannot resolve a dependency offline | Run `mvn -q dependency:go-offline` once with the internet on. |
| A run was interrupted | Drop the database named in `starter/target/lab-database.txt`, for example `psql -h localhost -d postgres -c "DROP DATABASE relational_design_lab_3f9c0a1b7d2e;"` with the name from the file. |

## Tested with

PostgreSQL 18.3, JDK 25 and Maven 3.9.9 on macOS (arm64), with no-password and with password-file connections. Linux and Windows runs have not been recorded yet; the steps follow PostgreSQL's documented behaviour there.
