import hashlib
from typing import Any, Dict, List, Optional

from src.decoder import decode_bencode


class TorrentFile:
    def __init__(
        self,
        announce: str,
        info_hash: bytes,
        piece_length: int,
        pieces: List[bytes],
        name: str,
        length: Optional[int] = None,
        files: Optional[List[Dict[str, Any]]] = None,
    ):
        self.announce = announce
        self.info_hash = info_hash
        self.piece_length = piece_length
        self.pieces = pieces
        self.name = name
        self.length = length  # For single-file torrents
        self.files = files  # For multi-file torrents
        self.is_multi_file = files is not None

    def __str__(self) -> str:
        if self.is_multi_file:
            return f"Torrent: {self.name} ({len(self.files)} files, {len(self.pieces)} pieces)"
        else:
            return (
                f"Torrent: {self.name} ({self.length} bytes, {len(self.pieces)} pieces)"
            )


def parse_torrent_file(torrent_path: str) -> TorrentFile:
    """
    Parse a .torrent file and return a TorrentFile object.
    """
    # Read the file and decode the bencoded data
    with open(torrent_path, "rb") as f:
        torrent_data = f.read()

    # Decode the bencoded data
    # Note: We need to decode bytes to string for our decoder
    decoded_data = decode_bencode(torrent_data.decode("latin-1"))

    if not isinstance(decoded_data, dict):
        raise ValueError("Invalid torrent file: root is not a dictionary")

    # Extract the required fields
    announce = decoded_data.get("announce")
    info = decoded_data.get("info")

    if not announce or not info:
        raise ValueError("Invalid torrent file: missing required fields")

    # Calculate the info hash
    # We need to re-encode the info dictionary to get the correct hash
    info_encoded = bencode(info).encode("latin-1")
    info_hash = hashlib.sha1(info_encoded).digest()

    # Extract info fields
    piece_length = info.get("piece length")
    pieces_str = info.get("pieces")
    name = info.get("name")

    if not piece_length or not pieces_str or not name:
        raise ValueError("Invalid torrent file: missing required info fields")

    # Split the pieces string into 20-byte SHA-1 hashes
    pieces = [pieces_str[i : i + 20] for i in range(0, len(pieces_str), 20)]

    # Check if this is a single file or multi-file torrent
    if "length" in info:
        # Single file torrent
        length = info["length"]
        return TorrentFile(announce, info_hash, piece_length, pieces, name, length)
    elif "files" in info:
        # Multi-file torrent
        files = info["files"]
        return TorrentFile(announce, info_hash, piece_length, pieces, name, files=files)
    else:
        raise ValueError("Invalid torrent file: neither single nor multi-file")


def bencode(data):
    """
    Encode a Python object into a bencoded string.
    """
    if isinstance(data, str):
        return f"{len(data)}:{data}"
    elif isinstance(data, int):
        return f"i{data}e"
    elif isinstance(data, list):
        return f"l{''.join(bencode(item) for item in data)}e"
    elif isinstance(data, dict):
        # Sort keys for canonical ordering
        sorted_items = sorted(data.items())
        return (
            f"d{''.join(bencode(key) + bencode(value) for key, value in sorted_items)}e"
        )
    else:
        raise ValueError(f"Cannot bencode data of type {type(data)}")
