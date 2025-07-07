def encode_int(value: int) -> bytes:
    return f"i{value}e".encode()


def encode_bytes(value: bytes) -> bytes:
    return f"{len(value)}:".encode() + value


def encode_dict(value: dict) -> bytes:
    return (
        b"d"
        + b"".join(bencode_encode(k) + bencode_encode(v) for k, v in value.items())
        + b"e"
    )


def encode_list(value: list) -> bytes:
    return b"l" + b"".join(bencode_encode(v) for v in value) + b"e"


def encode_str(value: str) -> bytes:
    return f"{len(value)}:{value}".encode()


def bencode_encode(value: dict | list | str | int | bytes) -> bytes:
    if isinstance(value, bytes):
        return encode_bytes(value)
    elif isinstance(value, dict):
        return encode_dict(value)
    elif isinstance(value, list):
        return encode_list(value)
    elif isinstance(value, str):
        return encode_str(value)
    elif isinstance(value, int):
        return encode_int(value)
    else:
        raise TypeError(f"Unsupported type: {type(value)}")
