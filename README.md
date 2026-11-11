# Relational design lab: a course enrollment schema

Turn a user story into a PostgreSQL schema. You write one file, `starter/schema.sql`, with three `CREATE TABLE` statements. Public JUnit tests load it into a new database on your own PostgreSQL server and check it against the story's acceptance criteria, by trying inserts and deletes that must be accepted or rejected.

You decide the design: which column is each table's key, which table holds the foreign keys, which data type suits each column, and which constraints and defaults make PostgreSQL enforce each criterion. Any suitable design passes; the tests check behaviour, not one particular way of writing it.

This lab practises the Relational Design topics *Tables, keys and relationships*, *Designing tables from a user story* and *CREATE TABLE, data types and constraints*. It uses no containers: only your local PostgreSQL server, a JDK and Maven.

About 10 minutes of setup the first time, then about 30 minutes for the tasks.

## Prerequisites

You need a running local PostgreSQL server (see the reading *Installing Postgres and a SQL client*), a JDK and Maven. Check each in a new terminal:

| Tool | Version | Check |
| --- | --- | --- |
| PostgreSQL server and `psql` | 18 (16 or later works) | the connection check below |
| JDK | 25 | `java -version` |
| Apache Maven | 3.9 or later | `mvn -v` |

**Connection check.** The tests connect with the PostgreSQL JDBC driver over TCP, to a host name and port, never through a local socket file. A plain `psql` can succeed through a socket while a TCP connection fails, so check with the same host, port, user and database the tests will use:

```
psql -h localhost -p 5432 -d postgres -c "SELECT version();"
```

Like the tests, `psql` takes the user from `PGUSER`, or else your login name. If you set `PGHOST`, `PGPORT` or `PGDATABASE` in Setup step 2, put the same values after `-h`, `-p` and `-d`. The check is done when it prints one row starting `PostgreSQL 18` (or 16, 17) without asking for a password. If it asks for a password, finish Setup step 2 first; if it fails, see Troubleshooting.

## Setup

1. Open a terminal in this lab's `starter/` folder.
2. Tell the tests how to reach your server, if the defaults do not fit. The tests read the same environment variables as `psql`:

   | Variable | Meaning | Default when unset |
   | --- | --- | --- |
   | `PGHOST` | server host name or IP address (not a socket directory) | `localhost` |
   | `PGPORT` | server port | `5432` |
   | `PGUSER` | PostgreSQL user; it must be allowed to create databases | your login name |
   | `PGDATABASE` | an existing database to connect to while creating the lab database | `postgres` |

   Set only the ones you need, in the same terminal, for example `export PGUSER=postgres` (macOS or Linux) or `$env:PGUSER = "postgres"` (Windows PowerShell).

   **If your server asks for a password**, store it in a password file, which both `psql` and the tests read. Each line has the form `host:port:database:user:password`; for this lab use `localhost:5432:*:postgres:your-password`, with your own port, PostgreSQL user and password.

   - macOS or Linux: write that line into `~/.pgpass`, then run `chmod 600 ~/.pgpass` so only you can read it (`psql` ignores a password file that others can read).
   - Windows: write that line into `%APPDATA%\postgresql\pgpass.conf` (create the `postgresql` folder if it is missing). Your user profile folder is private to you by default; keep it that way.

   The connection check now runs without asking for a password. Never write a password into `schema.sql` or any file you share.

   The tests also accept a `PGPASSWORD` environment variable, but PostgreSQL recommends against it: on some systems other users can read a process's environment. If you use it, use it only for a throwaway local account used for nothing else, and only in this terminal.
3. Download the test libraries once (needs the internet):

   ```
   mvn -q dependency:go-offline
   ```

After this step the test command works offline.

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

## Tasks

Work in `starter/schema.sql`, one table at a time. After each change, run the test command from `starter/` (see Test). Each task names the test that tells you when it is done; failing messages start with the criterion number they check, so you know which rule to revisit.

1. **Create the three tables.**
   1. Where: `starter/schema.sql`, below the comment lines.
   2. What: write one `CREATE TABLE` statement for each table in the names table, with every listed column. Give each column the data type you choose for it now; you can refine types and add constraints in the next tasks. Create `students` and `courses` before `enrollments`, because a foreign key can only point at a table that already exists.
   3. Expect: until all three tables and ten columns exist, `task1Tables` fails with `schema.sql must create a table named ...` or `Table ... has no column named ...`. If the file has an SQL mistake, every test reports `schema.sql did not run:` followed by PostgreSQL's message; fix that first.
   4. Done: `task1Tables` no longer appears in the failures.
2. **Make `students` meet criterion 1.**
   1. Where: your `students` statement.
   2. What: read criterion 1 and decide, for each column, which data type fits the values it describes, and which rules PostgreSQL must enforce: which column identifies a student, which values are required, which must be unique, and how a name longer than 100 characters is refused.
   3. Expect: `task2Students` fails with a `Criterion 1 (students):` message naming the rule that is missing, followed by the test's insert and, when PostgreSQL rejected it, its error.
   4. Done: `task2Students` no longer appears in the failures.
3. **Make `courses` meet criterion 2.**
   1. Where: your `courses` statement.
   2. What: decide which column identifies a course and what type suits a code like `SQL101`, which columns are required, and how to refuse a capacity that is not greater than 0.
   3. Expect: `task3Courses` fails with a `Criterion 2 (courses):` message naming the rule that is missing.
   4. Done: `task3Courses` no longer appears in the failures.
4. **Connect students and courses (criteria 3 and 5).**
   1. Where: your `enrollments` statement.
   2. What: classify the relationship between students and courses, then decide which columns must refer to which table, which of them are required, and which combination of columns must be unique so a student cannot enroll in the same course twice. Use column types that match the columns they refer to.
   3. Expect: `task4EnrollmentKeys` fails with a `Criterion 3 (many-to-many):` or `Criterion 5 (existing student and course):` message naming the insert or delete that was wrongly accepted or rejected.
   4. Done: `task4EnrollmentKeys` no longer appears in the failures.
5. **Record when and how well (criterion 4).**
   1. Where: the `enrolled_at` and `grade` columns of `enrollments`.
   2. What: choose a type that holds both a date and a time of day, make it required, and give it a default so PostgreSQL fills in the current time; choose an exact decimal type that keeps two decimal places for `grade`, allow it to be empty, and refuse values outside 0 to 100.
   3. Expect: `task5EnrollmentDefaults` fails with a `Criterion 4 (enrollment time and grade):` message naming the behaviour that is missing.
   4. Done: `task5EnrollmentDefaults` no longer appears in the failures, and the whole run matches Expected output.

**Starting over.** To restart from the shipped starter, first save your attempt somewhere else if you want to keep it, then delete every line of `starter/schema.sql` below its comment block (the shipped file contains only comments). The next test run fails all five tests again, exactly as it did at the start.

## Test

In `starter/`:

```
mvn -q -o test
```

Each run creates a new database with a unique name such as `relational_design_lab_3f9c0a1b7d2e`, runs your `schema.sql` in it, runs the tests, and drops that database again. It never removes a database it did not create: if a name is already taken, the run picks another. While a run is in progress, the name of its database is written to `starter/target/lab-database.txt`.

As shipped, `schema.sql` creates nothing, so all five tests fail; that is expected.

## Expected output

When every task is done, `mvn -q -o test` exits with status 0 and its report shows no failures. Check both:

- Exit status: `echo $?` (macOS or Linux) or `$LASTEXITCODE` (Windows PowerShell), run right after the test command, prints `0`.
- Test report: `starter/target/surefire-reports/relational.SchemaTest.txt` begins with `Tests run: 5, Failures: 0, Errors: 0, Skipped: 0`.

Quiet mode (`-q`) hides Maven's progress, but your JDK or Maven may still print warnings such as `WARNING: A restricted method ...`; those are not test failures. The full expected summary is in `expected/test-summary.txt`.

## Offline note

Only the setup step downloads anything. The test command runs offline and talks only to your local PostgreSQL server.

## Cleanup

- The tests drop their own lab database when they finish.
- If a run was interrupted, `starter/target/lab-database.txt` still names its database. Drop exactly that database, then delete the file, for example on macOS or Linux: `psql -h localhost -d postgres -c "DROP DATABASE relational_design_lab_3f9c0a1b7d2e;"` with the name from the file. Do this before deleting `starter/target`.
- Delete `starter/target` to remove compiled classes and test reports.
- Setup also stores the pinned libraries in your local Maven repository (`~/.m2/repository` by default); that shared cache is kept for later labs.

## Troubleshooting

- **The connection check says `Connection refused` or `could not connect`**: the server is not running or listens on another port. Start it as the installation reading shows, and check the port your installer chose.
- **`Could not reach PostgreSQL to create the lab database`**: run the connection check with the same values you set; fix it until it prints the version, then run the tests again.
- **`PGHOST is set to "...", which is not a host name`**: the tests connect over TCP; set `PGHOST` to `localhost` or your server's host name.
- **`password authentication failed`** or **`no password was provided`**: check the password file line (host, port, user and password must match) and, on macOS or Linux, its `chmod 600` permissions; or check `PGUSER`.
- **`role "..." does not exist`**: your login name is not a PostgreSQL user; set `PGUSER` to one that is, such as `postgres`.
- **`permission denied to create database`**: use a user that may create databases, such as the `postgres` user an installer creates.
- **`schema.sql did not run: ... relation "students" does not exist`**: a foreign key points at a table created later in the file; create `students` and `courses` first.
- **Maven says a dependency cannot be resolved offline**: run the setup step once with the internet on.

## Tested on

The lab's starter and a completed schema were run on macOS (arm64) with PostgreSQL 18.3, JDK 25 and Maven 3.9.9, both with no-password (trust) local connections and with password authentication through a password file and through `PGPASSWORD`. Linux and Windows runs have not yet been recorded; the steps above follow PostgreSQL's documented behaviour on those systems.
