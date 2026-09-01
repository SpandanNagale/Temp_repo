from fastapi import Depends, FastAPI

from app.auth import require_merchant
from app.payments import router as payments_router

app = FastAPI(title="payments-api")
app.include_router(payments_router, dependencies=[Depends(require_merchant)])


@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}
