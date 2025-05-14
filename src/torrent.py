from typing import Any


class TorrentFile:
    def __init__(
        self,
        announce: str,
        info_hash: bytes,
        piece_length: int,
        pieces: list[bytes],
        name: str,
        length: int | None = None,
        files: list[dict[str, Any]] = [],
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
    # Your code here
    return TorrentFile(
        announce="",
        info_hash=b"",
        piece_length=0,
        pieces=[],
        name="",
        length=0,
        files=[],
    )
