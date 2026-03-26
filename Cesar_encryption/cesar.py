def caesar(text, shift):
    result = ""
    for char in text:
        # Handle only alphabet characters
        if char.isalpha():
            # Get ASCII code and normalize to 0-25 range
            ascii_offset = ord('A') if char.isupper() else ord('a')
            # Convert to 0-25 range, apply shift, wrap around with modulo, convert back
            shifted = (ord(char) - ascii_offset + shift)% 26  + ascii_offset
            result += chr(shifted)
        else:
            # Keep non-alphabet characters unchanged
            result += char
    return result

# Example usage
message = "mohamed"
code = 3
encrypted = caesar(message, code)
print(encrypted)  
