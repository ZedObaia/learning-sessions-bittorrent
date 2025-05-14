from src.decoder import decode_bencode


def test_string_parsing():
    assert decode_bencode("4:spam") == "spam"


def test_integer_parsing():
    assert decode_bencode("i42e") == 42
    assert decode_bencode("i-42e") == -42


def test_list_parsing():
    assert decode_bencode("l4:spami42ee") == ["spam", 42]


def test_dictionary_parsing():
    assert decode_bencode("d3:foo3:bar5:helloi52ee") == {"foo": "bar", "hello": 52}


def test_complex_parsing():
    assert decode_bencode("d4:spaml4:spamli42ee5:helloe") == {
        "spam": ["spam", 42],
        "hello": None,
    }
