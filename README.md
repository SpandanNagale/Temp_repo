# payments-api

Acme's payments service: charges, refunds and the merchant ledger. FastAPI + PostgreSQL.

## Run it

    make dev        # starts Postgres in Docker and the API on :8080
    make test       # unit tests (pytest); needs no database

## Layout

- `app/auth.py`: API key and JWT checks for every request
- `app/payments.py`: charges and refunds
- `app/ledger.py`: double-entry ledger writes
- `docs/`: architecture, on-call runbook

Owners: payments (Priya), auth (Karan). See docs/architecture.md.
