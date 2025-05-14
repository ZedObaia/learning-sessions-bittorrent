from src.torrent import parse_torrent_file


def test_parse_torrent_file():
    torrent = parse_torrent_file("tests/files/ubuntu.torrent")
    print(torrent)
    print(f"Tracker: {torrent.announce}")
    print(f"Info hash: {torrent.info_hash.hex()}")
    print(f"Piece length: {torrent.piece_length} bytes")
    print(f"Number of pieces: {len(torrent.pieces)}")
    assert False
