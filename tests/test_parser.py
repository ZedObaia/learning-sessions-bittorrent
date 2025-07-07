from src.parser import TorrentFile


def test_parse_torrent_file():
    torrent = TorrentFile("tests/files/ubuntu.torrent")

    assert torrent.announce == "https://torrent.ubuntu.com/announce"
    assert torrent.info_hash_hex == "8a19577fb5f690970ca43a57ff1011ae202244b8"
    assert torrent.piece_length == 262144
    assert len(torrent.pieces) == 23951


def test_tracker_response():
    torrent = TorrentFile("tests/files/sample.torrent")
    response = torrent.get_tracker_response()
    peers = response.peers
    ips = set(peer.ip for peer in peers)
    assert len(ips) == 3
    assert ips == {"165.232.38.164", "165.232.41.73", "165.232.35.114"}
    assert response.interval == 60
