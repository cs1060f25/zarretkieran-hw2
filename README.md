# NOTE

I accidentally did not create a repo from the forked template before starting hw2. I just committed my changes to the bugfix branch of the public template (zarretkieran-hw2 in cs1060f25) after forking the original repo. I created this repo after completing the assignment, so all the files are complete, but the commit history remains in zarretkieran-hw2. To be clear, my commit history is in zarretkieran-hw2 (https://github.com/cs1060f25/zarretkieran-hw2) which is a public template, but the deployable repo is this one, zarretkieran-hw2-.

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

- **Base64 endianness mismatch**: the original implementation encoded/decoded base64 using big-endian byte order, but the project/tests require **little-endian** (the convention used on Windows and macOS). This caused failing round-trip tests for larger integers. Fix: updated `api/index.py` to use little-endian for both encoding and decoding and to reject negative integers for base64 conversions.

- **Limited text parsing for English words**: `text_to_number` initially only recognized very small single-word numbers (e.g. "zero" through "ten"). This made phrase examples such as "forty two" fail. Fix: integrated `text2digits` to parse multi-word phrases (with a small single-word fallback).

- **Negative number behavior**: handling of negative numbers varied by output type in the original implementation. Tests were updated to assert sensible behavior, and base64 now rejects negative inputs explicitly.

If you want to reproduce the original failures, check out the `bugfix` branch history before the fixes (commits are available on the remote repository).

## Clear error messages

The API returns specific error messages to help users fix inputs quickly. Examples:

- Base64 decode: `Invalid base64 input: not a valid base64-encoded string`
- Base64 encode with negative: `Base64 does not support negative integers`
- Binary: `Invalid binary input: only digits 0 and 1 are allowed`
- Octal: `Invalid octal input: only digits 0-7 are allowed`
- Decimal: `Invalid decimal input: expected digits 0-9 (optionally prefixed by -)`
- Hexadecimal: `Invalid hexadecimal input: expected characters 0-9 and a-f`
- Text: `Invalid text input: could not parse number from '<your input>'`
- Types: `Invalid input type: <type>` or `Invalid output type: <type>`

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
