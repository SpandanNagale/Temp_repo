from fastapi.testclient import TestClient

from app.main import app
from app.auth import require_merchant

app.dependency_overrides[require_merchant] = lambda: "m_test"
client = TestClient(app)


def test_charge_then_refund() -> None:
    assert client.post("/v1/charges", json={"charge_id": "c1", "amount_paise": 5000, "customer": "u1"}).status_code == 200
    r = client.post("/v1/charges/c1/refund")
    assert r.json() == {"id": "c1", "refunded": 5000}


def test_refund_twice_is_conflict() -> None:
    client.post("/v1/charges", json={"charge_id": "c2", "amount_paise": 100, "customer": "u1"})
    client.post("/v1/charges/c2/refund")
    assert client.post("/v1/charges/c2/refund").status_code == 409
