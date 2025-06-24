from src.decoder import decode_bencode


def test_string_parsing():
    assert decode_bencode("4:spam") == "spam"
    assert decode_bencode("6:Bahram") == "Bahram"


def test_integer_parsing():
    assert decode_bencode("i42e") == 42
    assert decode_bencode("i-42e") == -42


def test_list_parsing():
    assert decode_bencode("l4:spami42ee") == ["spam", 42]


def test_list_parsing_with_many_items():
    assert decode_bencode("l4:spami42e4:mmmmli42eee") == ["spam", 42, "mmmm", [42]]


def test_dictionary_parsing():
    assert decode_bencode("d3:foo3:bar5:helloi52ee") == {"foo": "bar", "hello": 52}
    assert decode_bencode("d3:cow3:moo4:spam4:eggs3:fooi42ee") == {
        "cow": "moo",
        "spam": "eggs",
        "foo": 42,
    }


def test_complex_parsing():
    assert decode_bencode("d4:spaml4:spami42ee5:hello5:worlde") == {
        "spam": ["spam", 42],
        "hello": "world",
    }
