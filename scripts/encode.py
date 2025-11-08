import sys


def decode(text: str, codec="latin-1") -> bytes:
    """Decode a string into bytes using the specified encoding format."""
    try:
        return text.encode(codec)
    except LookupError:
        print(f"Error: Unknown encoding format '{codec}'", file=sys.stderr)
        sys.exit(1)


def encode(data: bytes, codec="utf-8") -> str:
    """Encode bytes into a string using the specified encoding format."""
    try:
        return data.decode(codec)
    except LookupError:
        print(f"Error: Unknown encoding format '{codec}'", file=sys.stderr)
        sys.exit(1)


def convert(text: str, from_codec="latin-1", to_codec="utf-8") -> str:
    """Convert a string from one encoding format to another."""
    byte_data = decode(text, from_codec)
    return encode(byte_data, to_codec)
