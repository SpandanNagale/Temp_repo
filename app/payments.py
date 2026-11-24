"""Charges and refunds. Amounts are integers in paise; never floats."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ledger import transfer

router = APIRouter(prefix="/v1")
CHARGES: dict[str, dict] = {}  # stand-in for the charges table


class ChargeIn(BaseModel):
    charge_id: str
    amount_paise: int
    customer: str


class RefundIn(BaseModel):
    amount_paise: int | None = None  # None = refund what is left


@router.post("/charges")
def create_charge(body: ChargeIn) -> dict:
    if body.amount_paise <= 0:
        raise HTTPException(422, "amount must be positive")
    CHARGES[body.charge_id] = {"amount": body.amount_paise, "refunded": 0}
    transfer(f"customer:{body.customer}", "merchant", body.amount_paise, body.charge_id)
    return {"id": body.charge_id, "status": "succeeded"}


@router.post("/charges/{charge_id}/refund")
def refund(charge_id: str, body: RefundIn | None = None) -> dict:
    """Refund all or part of a charge."""
    charge = CHARGES.get(charge_id)
    if charge is None:
        raise HTTPException(404, "no such charge")
    amount = (body.amount_paise if body and body.amount_paise else charge["amount"])
    charge["refunded"] += amount
    transfer("merchant", "customer", amount, f"refund:{charge_id}")
    return {"id": charge_id, "refunded": charge["refunded"]}
