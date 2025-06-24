from typing import Any

"""
Bencoding is the encoding format used in .torrent files. It supports four data types:

- Strings: Length prefix followed by the string (e.g., `4:spam` = "spam")
- Integers: Start with 'i', followed by the number, and end with 'e' (e.g., `i42e` = 42)
- Lists: Start with 'l', followed by bencoded elements, and end with 'e' (e.g., `l4:spami42ee` = ["spam", 42])
- Dictionaries: Start with 'd', followed by alternating bencoded keys and values, and end with 'e' (e.g., `d3:foo3:bar5:helloi52ee` = {"foo": "bar", "hello": 52})

"""


def parse_bencoded_string(encoded_data: str, pos: int) -> tuple[str, int]:
    """
    Parse a bencoded string from the encoded_data starting at position pos.
    Returns the parsed string and the new position.
    """
    # Your code here
    length = int(encoded_data[pos])
    new_pos = pos + length + 2
    value = encoded_data[pos + 2 : new_pos]
    return value, new_pos


def parse_bencoded_integer(encoded_data: str, pos: int) -> tuple[int, int]:
    """
    Parse a bencoded integer from the encoded_data starting at position pos.
    Returns the parsed integer and the new position.
    - Integers: Start with 'i', followed by the number, and end with 'e' (e.g., `i42e` = 42)

    """
    pos += 1  # skip the 'i'
    end_pos = encoded_data.find("e", pos)
    num = int(encoded_data[pos:end_pos])
    return num, end_pos + 1


def parse_bencoded_list(encoded_data: str, pos: int) -> tuple[list, int]:
    """
    Parse a bencoded list from the encoded_data starting at position pos.
    Returns the parsed list and the new position.
    - Lists: Start with 'l', followed by bencoded elements, and end with 'e' (e.g., `l4:spami42ee` = ["spam", 42])

    """
    output = []
    cur_pos = pos + 1

    while encoded_data[cur_pos] != "e":
        value, cur_pos = decode_bencode_next(encoded_data, pos=cur_pos)
        output.append(value)

    return output, cur_pos + 1


def parse_bencoded_dict(encoded_data: str, pos: int) -> tuple[dict, int]:
    """
    Parse a bencoded dictionary from the encoded_data starting at position pos.
    Returns the parsed dictionary and the new position.
    - Dictionaries: Start with 'd', followed by alternating bencoded keys and values, and end with
      'e' (e.g., `d3:foo3:bar5:helloi52ee` = {"foo": "bar", "hello": 52})

    """
    output: dict[str, Any] = {}
    cur_pos = pos + 1  # Skip the 'd'

    while encoded_data[cur_pos] != "e":
        # Read the key (should always be a string in bencoding)
        key, cur_pos = decode_bencode_next(encoded_data, cur_pos)
        if not isinstance(key, str):
            raise ValueError(f"Dictionary key must be a string, got {type(key)}")

        # Read the value
        value, cur_pos = decode_bencode_next(encoded_data, cur_pos)

        # Add the key-value pair to the dictionary
        output[key] = value

    return output, cur_pos + 1  # Skip the 'e'


def decode_bencode_next(encoded_data: str, pos: int) -> tuple[object, int]:
    """
    Decode the next bencoded value from the encoded_data starting at position pos.
    Returns the decoded value and the new position.
    """
    if pos >= len(encoded_data):
        raise ValueError("Invalid bencoded data: unexpected end of data")

    char = encoded_data[pos]

    if char.isdigit():
        return parse_bencoded_string(encoded_data, pos)
    elif char == "i":
        return parse_bencoded_integer(encoded_data, pos)
    elif char == "l":
        return parse_bencoded_list(encoded_data, pos)
    elif char == "d":
        return parse_bencoded_dict(encoded_data, pos)
    else:
        raise ValueError(f"Invalid bencoded data: unknown type identifier '{char}'")


def decode_bencode(encoded_data: str) -> object:
    """
    Decode a bencoded string into a Python object.
    """
    value, pos = decode_bencode_next(encoded_data, 0)

    if pos != len(encoded_data):
        raise ValueError(
            f"Invalid bencoded data: extra data after decoded value, {pos=} and data {len(encoded_data)=}"
        )

    return value
