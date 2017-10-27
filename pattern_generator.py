"""
Simple random pattern generator script
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

def main():
    length = sys.argv[1]
    if length.isdigit():
        print pattern_generator(int(length))

if __name__ == "__main__":
    main()