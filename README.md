# Relational Design lab: a course enrollment schema

You design the database for a course coordinator: three PostgreSQL tables, `students`, `courses` and `enrollments`, that refuse bad data on their own.
You write them in one file, `src/main/sql/schema.sql`, and the tests load it into a fresh database and try inserts and deletes your tables must accept or reject.

You practise primary keys, foreign keys, unique and check constraints, defaults and choosing data types.

The full learner instructions are in [`.evolv/instructions.md`](.evolv/instructions.md), which the lab platform shows as the lab's instructions.

## Layout

This repository follows the Exa coding-lab scaffold for Java.

| Path | What it is |
|---|---|
| `src/main/sql/schema.sql` | Lab source: the schema the learner writes |
| `src/test/java/relational/SchemaTest.java` | Visible tests |
| `src/test/java/relational/LabDatabase.java` | Test support: creates and drops the run's own lab database |
| `.evolv/instructions.md` | Learner instructions |
| `.evolv/grade.yml` | Grading manifest, used by Run Tests and by the grader |
| `pom.xml` | Maven build: Java 17 and JUnit 5.11.3, matching the scaffold, plus the PostgreSQL JDBC driver |
| `Dockerfile` | Image for local Run Tests; warms the Maven cache |
| `expected/test-summary.txt` | The result of a finished lab |

There are no held-out tests in this lab: every test is visible.

## PostgreSQL prerequisite

The tests need a running PostgreSQL server (16 or later) that they reach over TCP.
They read `PGHOST`, `PGPORT`, `PGUSER` and `PGDATABASE` (defaults `localhost`, `5432`, the login user, `postgres`) and a password file or `PGPASSWORD`.
The user must be allowed to create databases: each run creates its own uniquely named database and drops it afterwards.
Without a reachable server every test fails with `Could not reach PostgreSQL to create the lab database`.

## Run the tests

On the platform, select **Run Tests**. From a terminal with JDK 17 or later, Apache Maven 3.9 and a reachable PostgreSQL server:

```
mvn -q test
```

All 5 tests fail until the schema is written. That is expected.
