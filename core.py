# assertions + utils
def assert_status_code(resp, expected):
    assert resp.status_code == expected, f"Expected {expected}, got {resp.status_code}. Body: {resp.text}"

def assert_quantity_in_range(value, min_v, max_v):
    assert min_v <= value <= max_v, f"Quantity {value} not in range {min_v}-{max_v}"

def extract_algorithm_traces(log_content):
    traces = []
    for line in log_content.splitlines():
        if "algorithmTrace" in line:
            try:
                traces.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return traces
