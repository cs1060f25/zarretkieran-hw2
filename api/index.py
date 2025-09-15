from flask import Flask, render_template, request, jsonify
from num2words import num2words
from text2digits import text2digits
import base64
import re
import binascii

app = Flask(__name__)

def text_to_number(text):
    """Convert English text number (including phrases) to integer"""
    # Remove non-letters except spaces and hyphens; lowercase for normalization
    clean_text = re.sub(r'[^a-zA-Z\s-]', '', text.lower())

    # Special case for zero
    if clean_text in ['zero', 'nil']:
        return 0

    # Try robust conversion using text2digits for phrases like "forty two"
    try:
        converter = text2digits.Text2Digits()
        numeric_text = converter.convert(clean_text)
        # Extract first integer (supports negative)
        match = re.search(r'-?\d+', numeric_text.replace(' ', ''))
        if match:
            return int(match.group(0))
    except Exception:
        pass

    # Fallback for simple single-word numbers
    number_words = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }
    if clean_text in number_words:
        return number_words[clean_text]

    raise ValueError("Unable to convert text to number")

def number_to_text(number):
    """Convert integer to English text"""
    try:
        return num2words(number)
    except:
        raise ValueError("Unable to convert number to text")

def base64_to_number(b64_str):
    """Convert base64 to integer (little-endian)"""
    try:
        decoded_bytes = base64.b64decode(b64_str, validate=True)
        return int.from_bytes(decoded_bytes, byteorder='little')
    except (binascii.Error, ValueError):
        raise ValueError("Invalid base64 input: not a valid base64-encoded string")

def number_to_base64(number):
    """Convert integer to base64 (little-endian)"""
    if number < 0:
        raise ValueError("Base64 does not support negative integers")
    byte_count = (number.bit_length() + 7) // 8
    number_bytes = number.to_bytes(byte_count, byteorder='little', signed=False)
    return base64.b64encode(number_bytes).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        input_value = data['input']
        input_type = data['inputType']
        output_type = data['outputType']
        
        # Convert input to integer based on input type
        if input_type == 'text':
            try:
                number = text_to_number(input_value)
            except Exception:
                raise ValueError(f"Invalid text input: could not parse number from '{input_value}'")
        elif input_type == 'binary':
            if not re.fullmatch(r'[01]+', str(input_value)):
                raise ValueError("Invalid binary input: only digits 0 and 1 are allowed")
            number = int(input_value, 2)
        elif input_type == 'octal':
            if not re.fullmatch(r'[0-7]+', str(input_value)):
                raise ValueError("Invalid octal input: only digits 0-7 are allowed")
            number = int(input_value, 8)
        elif input_type == 'decimal':
            if not re.fullmatch(r'-?\d+', str(input_value)):
                raise ValueError("Invalid decimal input: expected digits 0-9 (optionally prefixed by -)")
            number = int(input_value)
        elif input_type == 'hexadecimal':
            if not re.fullmatch(r'[0-9a-fA-F]+', str(input_value)):
                raise ValueError("Invalid hexadecimal input: expected characters 0-9 and a-f")
            number = int(input_value, 16)
        elif input_type == 'base64':
            number = base64_to_number(input_value)
        else:
            raise ValueError(f"Invalid input type: {input_type}")
            
        # Convert integer to output type
        if output_type == 'text':
            result = number_to_text(number)
        elif output_type == 'binary':
            result = bin(number)[2:]  # Remove '0b' prefix
        elif output_type == 'octal':
            result = oct(number)[2:]  # Remove '0o' prefix
        elif output_type == 'decimal':
            result = str(number)
        elif output_type == 'hexadecimal':
            result = hex(number)[2:]  # Remove '0x' prefix
        elif output_type == 'base64':
            result = number_to_base64(number)
        else:
            raise ValueError(f"Invalid output type: {output_type}")
            
        return jsonify({'result': result, 'error': None})
    except Exception as e:
        return jsonify({'result': None, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
