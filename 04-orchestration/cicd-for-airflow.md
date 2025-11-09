# CI/CD for Airflow

- Store DAGs as code; use pull requests and reviews.
- Static checks: flake8/ruff, isort, mypy; import DAG without executing tasks in tests.
- Unit tests for operators; integration tests with LocalExecutor.
- Deploy via artifact (wheel) or Git-Sync; keep dependencies pinned.
- Use canary deployments and backfill strategies.
