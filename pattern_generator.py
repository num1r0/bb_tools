"""
Simple random pattern generator script

TO DO:
    - Add buffer size computation function (used for EIP detection)
"""

import sys
from string import ascii_uppercase, ascii_lowercase, digits

def pattern_generator(length):
    """
    Pattern generator function. Generates up to 20278 bytes
    """
    pattern = ""
    for upper_char in ascii_uppercase:
        for lower_char in ascii_lowercase:
            for digit in digits:
                if len(pattern) < length:
                    pattern += upper_char + lower_char + digit
                else:
                    return pattern[:length]

def get_buffer_size(address):
    """
    Gets little endian memory address and finds buffer size
    """
    if address[:2] == "0x":
        address = address[2:]
        ascii_block = address.decode("hex")
        pattern = ""
        for upper_char in ascii_uppercase:
            for lower_char in ascii_lowercase:
                for digit in digits:
                    pattern += upper_char + lower_char + digit
                    buffer_size = pattern.find(ascii_block)
                    if buffer_size > -1:
                        return buffer_size
    else:
        print "Little Endian memory address expected (ex.: 0x41424344)"
        

def main():
    user_input = sys.argv[1]
    if user_input.isdigit():
        print pattern_generator(int(user_input))
    else:
        print get_buffer_size(str(user_input))

if __name__ == "__main__":
    main()