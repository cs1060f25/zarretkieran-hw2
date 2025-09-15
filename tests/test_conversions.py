import base64
import json
import itertools
import pytest


INPUT_TYPES = ["text", "binary", "octal", "decimal", "hexadecimal", "base64"]
OUTPUT_TYPES = ["text", "binary", "octal", "decimal", "hexadecimal", "base64"]


def int_to_base64_le(value: int) -> str:
    if value < 0:
        raise ValueError("negative not supported for base64")
    if value == 0:
        return ""  # zero length per little-endian minimal encoding
    # minimal little-endian byte representation (no sign)
    length = (value.bit_length() + 7) // 8
    little = value.to_bytes(length, byteorder="little", signed=False)
    return base64.b64encode(little).decode("utf-8")


def base64_le_to_int(b64: str) -> int:
    data = base64.b64decode(b64)
    if len(data) == 0:
        return 0
    return int.from_bytes(data, byteorder="little", signed=False)


def make_payload(input_value, input_type, output_type):
    return {
        "input": input_value,
        "inputType": input_type,
        "outputType": output_type,
    }


@pytest.mark.parametrize("n", [0, 1, 2, 5, 10, 42, 255, 256, 1024, 65535])
def test_all_input_to_all_output_roundtrip(client, n):
    # Prepare canonical representations for each type based on integer n using our little-endian convention for base64
    words = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
    }
    representations = {
        "text": words.get(n),  # text input only supports 0-10 per implementation
        "binary": bin(n)[2:],
        "octal": oct(n)[2:],
        "decimal": str(n),
        "hexadecimal": hex(n)[2:],
        "base64": int_to_base64_le(n),
    }

    for input_type, output_type in itertools.product(INPUT_TYPES, OUTPUT_TYPES):
        # Skip cases where we do not have a valid text input representation
        if input_type == "text" and representations["text"] is None:
            continue

        # Build the input value for the chosen input type
        input_value = representations[input_type]

        resp = client.post("/convert", json=make_payload(input_value, input_type, output_type))
        assert resp.status_code == 200
        payload = resp.get_json()

        if payload["error"]:
            # For supported n and supported paths, we do not expect errors
            pytest.fail(f"Unexpected error for {input_type}->{output_type}: {payload['error']}")

        result = payload["result"]

        # Validate the result decodes back to the original integer for each output_type
        if output_type == "text":
            # For small numbers we expect a non-empty string
            assert isinstance(result, str)
            assert len(result) > 0
        elif output_type == "binary":
            assert int(result, 2) == n
        elif output_type == "octal":
            assert int(result, 8) == n
        elif output_type == "decimal":
            assert int(result) == n
        elif output_type == "hexadecimal":
            assert int(result, 16) == n
        elif output_type == "base64":
            # Enforce little-endian per spec
            assert base64_le_to_int(result) == n


@pytest.mark.parametrize("word,n", [
    ("zero", 0),
    ("one", 1),
    ("two", 2),
    ("three", 3),
    ("four", 4),
    ("five", 5),
    ("six", 6),
    ("seven", 7),
    ("eight", 8),
    ("nine", 9),
    ("ten", 10),
])
def test_text_inputs_basic_words_to_all_outputs(client, word, n):
    for output_type in OUTPUT_TYPES:
        resp = client.post("/convert", json=make_payload(word, "text", output_type))
        assert resp.status_code == 200
        payload = resp.get_json()
        assert payload["error"] is None

        if output_type == "text":
            assert isinstance(payload["result"], str) and len(payload["result"]) > 0
        elif output_type == "binary":
            assert int(payload["result"], 2) == n
        elif output_type == "octal":
            assert int(payload["result"], 8) == n
        elif output_type == "decimal":
            assert int(payload["result"]) == n
        elif output_type == "hexadecimal":
            assert int(payload["result"], 16) == n
        elif output_type == "base64":
            assert base64_le_to_int(payload["result"]) == n


def test_homepage_loads(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Numeric Converter" in r.data


