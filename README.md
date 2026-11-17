# Relational Design lab: a course enrollment schema

You design the database for a course coordinator: three PostgreSQL tables, `students`, `courses` and `enrollments`, that refuse bad data on their own.
You write them in one file, `src/schema.sql`.
The tests load your file into a fresh PostgreSQL database and try inserts and deletes that your tables must accept or reject.

**Time:** about 30 minutes.

You need no database server of your own: the tests start a private PostgreSQL 16 for each run and delete it afterwards.

## Quick start

1. Open `src/schema.sql`. It holds only comments.
2. Select **Run Tests** before you change anything.

   **All 5 visible tests fail at first. That is expected: the file holds no tables yet.**
   Each failure names the task, table, column or criterion to fix next.
3. Work through the checklist below. After each task, select **Run Tests** again and read the remaining failures.
4. **You are finished when all 5 visible tests pass.** Then select **Submit**.
   Submitting also runs held-out tests you can't see. They try the edge cases of each criterion, so meet every criterion in full, not only the cases the visible tests try.

```
OPEN schema.sql -> RUN TESTS: 5 fail (expected)
  -> READ the failures -> EDIT the next task -> RUN TESTS again
  -> repeat for Tasks 1-5 -> SUBMIT when all 5 tests pass
```

In words: open the file, run the tests, read which tasks fail, complete one task, run the tests again, and submit when they all pass.

## Checklist

All five tasks are in `src/schema.sql`. Read [the user story](#the-user-story) first.

- [ ] Task 1: create the three tables (test `test_task1_tables`)
- [ ] Task 2: make `students` meet criterion 1 (test `test_task2_students`)
- [ ] Task 3: make `courses` meet criterion 2 (test `test_task3_courses`)
- [ ] Task 4: connect students and courses, criteria 3 and 5 (test `test_task4_enrollment_keys`)
- [ ] Task 5: record when and how well, criterion 4 (test `test_task5_enrollment_defaults`)

A task is done when its test passes.
Edit only `schema.sql`. The tests in `test/` are restored to their original state before your work is graded, so changes to them do not count.

From a terminal in the project folder, you can run one task's test on its own, for example `python -m pytest -q -k task1`, or all of them with `python -m pytest -q`.

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

Decide which columns must refer to which table, which of them are required, and which combination of columns must be unique so a student cannot enroll in the same course twice. Use column types that match the columns they refer to. Criterion 5 also says what happens when someone tries to delete a student who has enrollments.

</details>

### Task 5: record when and how well (criterion 4)

Work on the `enrolled_at` and `grade` columns. A failure starts with `Criterion 4 (enrollment time and grade):`.

<details><summary>Hint</summary>

For `enrolled_at`, choose a type that holds a date and a time of day, make it required, and give it a default so PostgreSQL fills in the current time. For `grade`, choose an exact decimal type that keeps two decimal places, allow it to be empty, and refuse values outside 0 to 100.

</details>

**Starting over:** delete every line of `schema.sql` below its comment block. The shipped file holds only comments, so all five tests fail again.

## Try it by hand (optional, not tested)

`python -m test.practice src/schema.sql` starts a private PostgreSQL, runs your file in a new, empty database, and opens a `psql` prompt on it.
Try inserts the criteria should accept or reject, and use `\d students` to see a table's columns and constraints.
Leave with `\q`: the practice database is deleted, so the next start is fresh.

## What the tests do

The first test starts a private PostgreSQL 16 from the `pgserver` package in a temporary folder.
Every test then gets its own new, empty database, runs your `schema.sql` in it, tries its inserts and deletes, and drops that database.
At the end of the run the server and its folder are deleted. The tests never connect to any other database.

## Using an AI assistant

If you use an AI assistant, ask it to explain, not to answer.
"Explain what a composite primary key does" teaches you design; "write my schema" does not.
Check any explanation with a test run before you trust it.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| `pgserver package, which is not installed` | Run `python -m pip install -r requirements.txt`. `pgserver` needs Python 3.9 to 3.12; **Run Tests** uses a supported Python. |
| `schema.sql did not run: ... relation "students" does not exist` | A foreign key points at a table created later in the file. Create `students` and `courses` first. |
| `schema.sql did not run: ... syntax error` | Read the line PostgreSQL quotes. A missing comma between columns or a missing semicolon between statements is the usual cause. |
| `This statement should be rejected by a rule for that criterion, but the error was different` | PostgreSQL refused the row for another reason, for example a type that cannot hold the value. Read its message and fix that column first. |
