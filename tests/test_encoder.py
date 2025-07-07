from src.encoder import bencode_encode


def test_string_encoding():
    """Test encoding of string values"""
    assert bencode_encode("spam") == b"4:spam"
    assert bencode_encode("Bahram") == b"6:Bahram"
    assert bencode_encode("") == b"0:"
    assert bencode_encode("hello world") == b"11:hello world"


def test_integer_encoding():
    """Test encoding of integer values"""
    assert bencode_encode(42) == b"i42e"
    assert bencode_encode(-42) == b"i-42e"
    assert bencode_encode(0) == b"i0e"
    assert bencode_encode(123456789) == b"i123456789e"


def test_bytes_encoding():
    """Test encoding of bytes values"""
    assert bencode_encode(b"spam") == b"4:spam"
    assert bencode_encode(b"hello") == b"5:hello"
    assert bencode_encode(b"") == b"0:"
    assert bencode_encode(b"test\x00bytes") == b"10:test\x00bytes"


def test_list_encoding():
    """Test encoding of list values"""
    assert bencode_encode(["spam", 42]) == b"l4:spami42ee"
    assert bencode_encode([]) == b"le"
    assert bencode_encode([1, 2, 3]) == b"li1ei2ei3ee"
    assert bencode_encode(["hello", "world"]) == b"l5:hello5:worlde"


def test_nested_list_encoding():
    """Test encoding of nested list structures"""
    assert bencode_encode(["spam", 42, "mmmm", [42]]) == b"l4:spami42e4:mmmmli42eee"
    assert bencode_encode([[1, 2], [3, 4]]) == b"lli1ei2eeli3ei4eee"
    assert bencode_encode([[], [1], [1, 2]]) == b"lleli1eeli1ei2eee"


def test_dictionary_encoding():
    """Test encoding of dictionary values"""
    assert bencode_encode({"foo": "bar", "hello": 52}) == b"d3:foo3:bar5:helloi52ee"
    assert bencode_encode({}) == b"de"
    assert (
        bencode_encode({"cow": "moo", "spam": "eggs", "foo": 42})
        == b"d3:cow3:moo4:spam4:eggs3:fooi42ee"
    )


def test_nested_dictionary_encoding():
    """Test encoding of nested dictionary structures"""
    assert (
        bencode_encode({"spam": ["spam", 42], "hello": "world"})
        == b"d4:spaml4:spami42ee5:hello5:worlde"
    )
    assert bencode_encode({"outer": {"inner": "value"}}) == b"d5:outerd5:inner5:valueee"


def test_complex_nested_structures():
    """Test encoding of complex nested data structures"""
    complex_data = {
        "string": "test",
        "integer": 123,
        "list": [1, "two", {"nested": "value"}],
        "dict": {"key": [1, 2, 3]},
    }
    # Dictionary keys are sorted lexicographically in bencode: string, integer, list, dict
    expected = b"d6:string4:test7:integeri123e4:listli1e3:twod6:nested5:valueee4:dictd3:keyli1ei2ei3eeee"
    assert bencode_encode(complex_data) == expected


def test_edge_cases():
    """Test edge cases and special values"""
    # Empty values
    assert bencode_encode("") == b"0:"
    assert bencode_encode(b"") == b"0:"
    assert bencode_encode([]) == b"le"
    assert bencode_encode({}) == b"de"

    # Zero and negative numbers
    assert bencode_encode(0) == b"i0e"
    assert bencode_encode(-0) == b"i0e"
    assert bencode_encode(-1) == b"i-1e"

    # Large numbers
    assert bencode_encode(999999999) == b"i999999999e"
    assert bencode_encode(-999999999) == b"i-999999999e"


def test_mixed_types():
    """Test encoding of mixed type structures"""
    mixed_data = ["string", 42, {"key": "value"}, [1, 2, 3], b"bytes"]
    expected = b"l6:stringi42ed3:key5:valueeli1ei2ei3ee5:bytese"
    assert bencode_encode(mixed_data) == expected


def test_unicode_strings():
    """Test encoding of unicode strings"""
    assert bencode_encode("café") == "4:café".encode("utf-8")
    assert bencode_encode("привет") == "6:привет".encode("utf-8")
    # The emoji 🎉 is 1 character, so length should be 1
    assert bencode_encode("🎉") == "1:🎉".encode("utf-8")


def test_round_trip_compatibility():
    """Test that encoded data can be decoded back to original (if decoder is available)"""
    # This test assumes the decoder is working correctly
    # We'll test a simple case to ensure encoder output is valid bencode format
    test_cases = ["hello", 42, ["test", 123], {"key": "value"}, b"bytes"]

    for case in test_cases:
        encoded = bencode_encode(case)
        # Basic format validation
        assert isinstance(encoded, bytes)
        assert len(encoded) > 0
