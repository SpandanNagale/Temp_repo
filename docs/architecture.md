# Architecture

Requests enter through `app/main.py`. Every route under `/v1` depends on
`require_merchant` (`app/auth.py`), which accepts either a merchant API key
(`Authorization: ApiKey <merchant>.<secret>`) or a dashboard JWT signed by
login.acme.in (`Authorization: Bearer <jwt>`).

Money never moves without a ledger pair: `app/ledger.py` `transfer()` writes a
debit and a matching credit. Amounts are integers in paise.

Ownership: payments and refunds belong to Priya Shah; authentication to Karan Mehta.
