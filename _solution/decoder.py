def parse_bencoded_string(encoded_data: str, pos: int) -> tuple[str, int]:
    """
    Parse a bencoded string from the encoded_data starting at position pos.
    Returns the parsed string and the new position.
    """
    colon_pos = encoded_data.find(":", pos)
    if colon_pos == -1:
        raise ValueError("Invalid bencoded string: no colon found")

    length = int(encoded_data[pos:colon_pos])
    string_start = colon_pos + 1
    string_end = string_start + length

    if string_end > len(encoded_data):
        raise ValueError("Invalid bencoded string: string length exceeds data length")

    return encoded_data[string_start:string_end], string_end


def parse_bencoded_integer(encoded_data: str, pos: int) -> tuple[int, int]:
    """
    Parse a bencoded integer from the encoded_data starting at position pos.
    Returns the parsed integer and the new position.
    """
    if encoded_data[pos] != "i":
        raise ValueError("Invalid bencoded integer: does not start with 'i'")

    end_pos = encoded_data.find("e", pos + 1)
    if end_pos == -1:
        raise ValueError("Invalid bencoded integer: no ending 'e' found")

    # Extract and convert the integer
    try:
        value = int(encoded_data[pos + 1 : end_pos])
    except ValueError:
        raise ValueError("Invalid bencoded integer: cannot convert to integer")

    return value, end_pos + 1


def parse_bencoded_list(encoded_data: str, pos: int) -> tuple[list, int]:
    """
    Parse a bencoded list from the encoded_data starting at position pos.
    Returns the parsed list and the new position.
    """
    if encoded_data[pos] != "l":
        raise ValueError("Invalid bencoded list: does not start with 'l'")

    result = []
    pos += 1  # Skip the 'l'

    while pos < len(encoded_data) and encoded_data[pos] != "e":
        value, pos = decode_bencode_next(encoded_data, pos)
        result.append(value)

    if pos >= len(encoded_data):
        raise ValueError("Invalid bencoded list: no ending 'e' found")

    return result, pos + 1  # Skip the 'e'


def parse_bencoded_dict(encoded_data: str, pos: int) -> tuple[dict, int]:
    """
    Parse a bencoded dictionary from the encoded_data starting at position pos.
    Returns the parsed dictionary and the new position.
    """
    if encoded_data[pos] != "d":
        raise ValueError("Invalid bencoded dictionary: does not start with 'd'")

    result = {}
    pos += 1  # Skip the 'd'

    while pos < len(encoded_data) and encoded_data[pos] != "e":
        # Keys in a dictionary must be strings
        key, pos = decode_bencode_next(encoded_data, pos)
        if not isinstance(key, str):
            raise ValueError("Invalid bencoded dictionary: key is not a string")

        value, pos = decode_bencode_next(encoded_data, pos)
        result[key] = value

    if pos >= len(encoded_data):
        raise ValueError("Invalid bencoded dictionary: no ending 'e' found")

    return result, pos + 1  # Skip the 'e'


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
        raise ValueError("Invalid bencoded data: extra data after decoded value")

    return value
