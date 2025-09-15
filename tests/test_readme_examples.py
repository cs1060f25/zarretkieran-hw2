import pytest


def post(client, payload):
    return client.post("/convert", json=payload)


def test_readme_example_decimal_to_binary(client):
    r = post(client, {"input": "42", "inputType": "decimal", "outputType": "binary"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["error"] is None
    assert int(data["result"], 2) == 42


def test_readme_example_text_to_decimal(client):
    r = post(client, {"input": "forty two", "inputType": "text", "outputType": "decimal"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["error"] is None
    assert int(data["result"]) == 42


def test_readme_example_hex_to_text(client):
    r = post(client, {"input": "2a", "inputType": "hexadecimal", "outputType": "text"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["error"] is None
    assert isinstance(data["result"], str) and len(data["result"]) > 0
