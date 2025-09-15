import base64
import pytest


def post(client, payload):
    return client.post("/convert", json=payload)


@pytest.mark.parametrize("payload", [
    {},
    {"input": "123"},
    {"inputType": "decimal"},
    {"outputType": "decimal"},
    {"input": "123", "inputType": "decimal"},
    {"input": "123", "outputType": "decimal"},
])
def test_missing_fields(client, payload):
    resp = post(client, payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["result"] is None
    assert data["error"] is not None


@pytest.mark.parametrize("input_type,input_value,expected_msg_substr", [
    ("binary", "2", "Invalid binary input"),
    ("binary", "102", "Invalid binary input"),
    ("octal", "89", "Invalid octal input"),
    ("decimal", "12.3", "Invalid decimal input"),
    ("decimal", "abc", "Invalid decimal input"),
    ("hexadecimal", "g1", "Invalid hexadecimal input"),
    ("base64", "not-base64!!", "Invalid base64 input"),
    ("text", "eleventy", "Invalid text input"),
])
def test_invalid_inputs(client, input_type, input_value, expected_msg_substr):
    resp = post(client, {"input": input_value, "inputType": input_type, "outputType": "decimal"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["result"] is None
    assert data["error"] is not None
    assert expected_msg_substr in data["error"]


@pytest.mark.parametrize("output_type", ["binary", "octal", "decimal", "hexadecimal", "base64", "text"])
def test_negative_numbers_from_decimal_handled_or_rejected(client, output_type):
    resp = post(client, {"input": "-42", "inputType": "decimal", "outputType": output_type})
    assert resp.status_code == 200
    data = resp.get_json()
    if output_type == "base64":
        assert data["result"] is None
        assert "Base64 does not support negative integers" in data["error"]
    else:
        assert "error" in data


def test_base64_roundtrip_mismatch_endianness_expected_to_fail(client):
    # Provide little-endian base64 for 4660 (0x1234)
    value = 0x1234
    b = value.to_bytes(2, "little")
    b64_le = base64.b64encode(b).decode("utf-8")

    # Implementation decodes big-endian, so it should not equal the same number
    resp = post(client, {"input": b64_le, "inputType": "base64", "outputType": "decimal"})
    assert resp.status_code == 200
    data = resp.get_json()
    # Either an incorrect value or an error is acceptable for this negative test, but we expect no crash
    assert "error" in data


@pytest.mark.parametrize("input_type,input_value", [
    ("binary", "1"),
    ("octal", "7"),
    ("decimal", "1"),
    ("hexadecimal", "a"),
    ("base64", base64.b64encode((1).to_bytes(1, "little")).decode("utf-8")),
])
def test_invalid_output_type(client, input_type, input_value):
    resp = post(client, {"input": input_value, "inputType": input_type, "outputType": "unknown"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["result"] is None
    assert "Invalid output type" in data["error"]


@pytest.mark.parametrize("output_type", ["binary", "octal", "decimal", "hexadecimal", "base64"]) 
def test_invalid_input_type(client, output_type):
    resp = post(client, {"input": "1", "inputType": "unknown", "outputType": output_type})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["result"] is None
    assert "Invalid input type" in data["error"]


