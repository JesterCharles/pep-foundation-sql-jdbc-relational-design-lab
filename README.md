# Relational Design — Code lab

Design a course-enrollment schema: three PostgreSQL tables with keys and constraints that refuse bad data on their own.

- **Edit:** `src/schema.sql`. The file starts as comments only; write the three CREATE TABLE statements.
- **Run the tests:** **Run Tests** in Exa Studio, or `pip install -r requirements.txt` then `python -m pytest -q`. All 5 visible tests fail at first; each message names the table or column to fix.
- **No database to install:** the tests start a private PostgreSQL 16 (via `pgserver`, Python 3.9-3.12) and delete it afterwards. `python -m test.practice src/schema.sql` opens a `psql` prompt to try queries by hand.
- **Done** when every visible test passes. **Submit** also runs held-out tests you can't see.

Full task steps and hints: [`.evolv/instructions.md`](.evolv/instructions.md)
