def _parse_bencoded_string(encoded_data: bytes, pos: int) -> tuple[str | bytes, int]:
    """
    Parse a bencoded string from the encoded_data starting at position pos.
    Returns the parsed string (as str if valid UTF-8, otherwise as bytes) and the new position.
    """
    # Find the colon that separates length from content
    colon_pos = encoded_data.find(b":", pos)
    if colon_pos == -1:
        raise ValueError("Invalid bencoded string: missing colon")

    # Parse the length
    length = int(encoded_data[pos:colon_pos].decode("ascii"))

    # Extract the content
    start_pos = colon_pos + 1
    end_pos = start_pos + length
    raw_value = encoded_data[start_pos:end_pos]

    # Try to decode as UTF-8, fall back to bytes if it fails
    try:
        value: str | bytes = raw_value.decode("utf-8")
    except UnicodeDecodeError:
        value = raw_value

    return value, end_pos


def _parse_bencoded_integer(encoded_data: bytes, pos: int) -> tuple[int, int]:
    """
    Parse a bencoded integer from the encoded_data starting at position pos.
    Returns the parsed integer and the new position.
    - Integers: Start with 'i', followed by the number, and end with 'e' (e.g., `i42e` = 42)

    """
    pos += 1  # skip the 'i'
    end_pos = encoded_data.find(b"e", pos)
    if end_pos == -1:
        raise ValueError("Invalid bencoded integer: missing 'e'")

    num = int(encoded_data[pos:end_pos].decode("ascii"))
    return num, end_pos + 1


def _parse_bencoded_list(encoded_data: bytes, pos: int) -> tuple[list, int]:
    """
    Parse a bencoded list from the encoded_data starting at position pos.
    Returns the parsed list and the new position.
    - Lists: Start with 'l', followed by bencoded elements, and end with 'e' (e.g., `l4:spami42ee` = ["spam", 42])

    """
    output = []
    cur_pos = pos + 1

    while cur_pos < len(encoded_data) and encoded_data[cur_pos : cur_pos + 1] != b"e":
        value, cur_pos = _decode_bencode_next(encoded_data, pos=cur_pos)
        output.append(value)

    return output, cur_pos + 1


def _parse_bencoded_dict(encoded_data: bytes, pos: int) -> tuple[dict, int]:
    """
    Parse a bencoded dictionary from the encoded_data starting at position pos.
    Returns the parsed dictionary and the new position.
    - Dictionaries: Start with 'd', followed by alternating bencoded keys and values, and end with
      'e' (e.g., `d3:foo3:bar5:helloi52ee` = {"foo": "bar", "hello": 52})

    """
    output: dict[str | bytes, Any] = {}
    cur_pos = pos + 1  # Skip the 'd'

    while cur_pos < len(encoded_data) and encoded_data[cur_pos : cur_pos + 1] != b"e":
        # Read the key (should always be a string or bytes in bencoding)
        key, cur_pos = _decode_bencode_next(encoded_data, cur_pos)
        if not isinstance(key, (str, bytes)):
            raise ValueError(
                f"Dictionary key must be a string or bytes, got {type(key)}"
            )

        # Read the value
        value, cur_pos = _decode_bencode_next(encoded_data, cur_pos)

        # Add the key-value pair to the dictionary
        output[key] = value

    return output, cur_pos + 1  # Skip the 'e'


def _decode_bencode_next(encoded_data: bytes, pos: int) -> tuple[object, int]:
    """
    Decode the next bencoded value from the encoded_data starting at position pos.
    Returns the decoded value and the new position.
    """
    if pos >= len(encoded_data):
        raise ValueError("Invalid bencoded data: unexpected end of data")

    char = encoded_data[pos : pos + 1]

    if char.isdigit():
        return _parse_bencoded_string(encoded_data, pos)
    elif char == b"i":
        return _parse_bencoded_integer(encoded_data, pos)
    elif char == b"l":
        return _parse_bencoded_list(encoded_data, pos)
    elif char == b"d":
        return _parse_bencoded_dict(encoded_data, pos)
    else:
        raise ValueError(f"Invalid bencoded data: unknown type identifier {char!r}")


def decode_bencode(bencoded_value):
    value, pos = _decode_bencode_next(bencoded_value, 0)

    if pos != len(bencoded_value):
        raise ValueError(
            f"Invalid bencoded data: extra data after decoded value, {pos=} and data {len(bencoded_value)=}"
        )

    return value
