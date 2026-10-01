# PySpark CI with GitHub Actions

A PySpark data-cleaning job with unit tests that run automatically on every Pull Request using GitHub Actions.

## What the job does

`clean_data(df)` in `pyspark_job.py`:
- Removes rows where `amount <= 0`
- Removes rows where `name` is NULL
- Adds `amount_with_tax` = `amount * 1.20`

## Project structure

    .github/workflows/ci.yml   # CI workflow (runs on pull requests)
    pyspark_job.py             # clean_data implementation
    test_pyspark_job.py        # pytest unit tests
    requirements.txt           # pyspark, pytest

## Running locally

Requires Python 3.10 or 3.11 and Java 17.

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    pytest -v

## CI

GitHub Actions runs the test suite whenever a Pull Request is opened, reopened, or updated with new commits.