# On-call runbook

- Refund failures: check the ledger pair for `refund:<charge id>` first.
- 401 spikes: usually an expired JWT signing key; rotate JWT_PUBLIC_KEY.
- Escalate payment-integrity issues to the payments owner within 30 minutes.
