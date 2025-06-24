from src.torrent import parse_torrent_file


def test_parse_torrent_file():
    torrent = parse_torrent_file("tests/files/ubuntu.torrent")

    assert torrent.announce == "https://torrent.ubuntu.com/announce"
    assert torrent.info_hash.hex() == "8a19577fb5f690970ca43a57ff1011ae202244b8"
    assert torrent.piece_length == 262144
    assert len(torrent.pieces) == 23951
