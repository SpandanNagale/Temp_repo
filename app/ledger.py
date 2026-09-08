"""Double-entry ledger: every money movement writes a balanced pair of entries."""

from dataclasses import dataclass


@dataclass
class Entry:
    account: str
    amount_paise: int  # positive = debit, negative = credit
    reference: str


def transfer(source: str, target: str, amount_paise: int, reference: str) -> list[Entry]:
    if amount_paise <= 0:
        raise ValueError("amount must be positive")
    return [Entry(source, -amount_paise, reference), Entry(target, amount_paise, reference)]
