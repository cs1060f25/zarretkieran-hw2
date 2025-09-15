# Numeric Converter - cs1060-hw2-base

A web-based application that converts numbers between different formats including:
- English text (e.g., "one hundred twenty-three")
- Binary
- Octal
- Decimal
- Hexadecimal
- Base64

## Setup

1. Install the required dependencies. We recommend following the best Python practice of a virtual environment. (This assumes Python3.)
```bash
python3 -m venv "hw2-env"
. hw2-env/bin/activate
pip3 install -r requirements.txt
```

2. Run the application:
```bash
python api/index.py
```

3. Open your web browser and navigate to `http://localhost:5000`

## Testing

Run the automated tests with pytest:

```bash
. hw2-env/bin/activate
pytest -q
```

Optionally, generate coverage:

```bash
pytest --cov=api --cov-report=term-missing
```

## Bugs encountered (before fixes)

The following issues were discovered while developing and testing this project and have been fixed on the `bugfix` branch.

- **Access denied on `http://localhost:5000` (HTTP 403)**: accessing `localhost:5000` returned a 403 while `127.0.0.1:5000` worked. Root cause: another process was bound to the IPv6/localhost address and returned 403 for requests routed to `localhost`. Workarounds/fixes applied: either stop the conflicting process or run the app on a different port or bind to all addresses. Tests/usage were adjusted to use `127.0.0.1` or an alternate port when appropriate.

- **Port already in use when starting the server**: attempting to start the server sometimes produced "Address already in use" due to existing Python processes listening on port 5000. Resolution: stop the conflicting processes (e.g. `kill <pid>`) or run the app on a different port (example: `--port 5001`).

- **Base64 endianness mismatch**: the original implementation encoded/decoded base64 using big-endian byte order, but the project/tests require **little-endian** (the convention used on Windows and macOS). This caused failing round-trip tests for larger integers. Fix: updated `api/index.py` to use little-endian for both encoding and decoding and to reject negative integers for base64 conversions.

- **Limited text parsing for English words**: `text_to_number` initially only recognized very small single-word numbers (e.g. "zero" through "ten"). This made phrase examples such as "forty two" fail. Fix: integrated `text2digits` to parse multi-word phrases (with a small single-word fallback).

- **Negative number behavior**: handling of negative numbers varied by output type in the original implementation. Tests were updated to assert sensible behavior, and base64 now rejects negative inputs explicitly.

If you want to reproduce the original failures, check out the `bugfix` branch history before the fixes (commits are available on the remote repository).

## Usage

1. Enter your input value in the text box
2. Select the input format from the dropdown menu
3. Select the desired output format from the second dropdown menu
4. Click "Convert" to see the result

## Examples

- Convert decimal to binary: Input "42" with input type "decimal" and output type "binary"
- Convert text to decimal: Input "forty two" with input type "text" and output type "decimal"
- Convert hexadecimal to text: Input "2a" with input type "hexadecimal" and output type "text"

# Deploying
The application should deploy to [Vercel](https://vercel.com?utm_source=github&utm_medium=readme&utm_campaign=vercel-examples) 
out of the box.

Just Add New... > Project, import the Git repository, and off you go.
Note that Vercel's Hobby plan means your private repository needs to be
in your personal GitHub account, not the organizational account.
