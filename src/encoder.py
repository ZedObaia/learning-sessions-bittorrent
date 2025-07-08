def encode_int(value: int) -> bytes:
    # TODO: Implement me
    raise NotImplementedError("encode_int not implemented")


def encode_bytes(value: bytes) -> bytes:
    # TODO: Implement me
    # hint: just encode it as a string, but do no need to convert the actual bytes, since it's already bytes!
    raise NotImplementedError("encode_bytes not implemented")


def encode_dict(value: dict) -> bytes:
    # TODO: Implement me
    # Hint: recursively call bencode_encode on each value
    raise NotImplementedError("encode_dict not implemented")


def encode_list(value: list) -> bytes:
    # TODO: Implement me
    # Hint: recursively call bencode_encode on each value
    raise NotImplementedError("encode_list not implemented")


def encode_str(value: str) -> bytes:
    # TODO: Implement me
    raise NotImplementedError("encode_str not implemented")


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
