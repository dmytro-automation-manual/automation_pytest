import pytest
from core import assert_status_code, assert_quantity_in_range, extract_algorithm_traces

# --- API tests ---
@pytest.mark.api
def test_create_order(api_client):
    payload = {"instrument": "SIM0001", "side": "BUY", "quantity": 100}
    resp = api_client.post("/orders", payload)
    assert_status_code(resp, 201)
    assert resp.json()["status"] == "ACCEPTED"

@pytest.mark.api
def test_get_order_status(api_client):
    resp = api_client.get("/orders/1")
    assert_status_code(resp, 200)
    data = resp.json()
    assert "status" in data

# --- Integration / logs ---
@pytest.mark.integration
def test_order_generation_logged(api_client, ssh_client):
    api_client.post("/generator/start", {})
    log_content = ssh_client.read_file("/var/log/simulator/app.log")
    traces = extract_algorithm_traces(log_content)
    assert traces, "No algorithm traces found"
    last_trace = traces[-1]
    qty = last_trace["step10"]["generatedQuantity"]
    assert_quantity_in_range(qty, 1, 1000)
