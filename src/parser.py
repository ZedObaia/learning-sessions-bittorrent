import dataclasses as _dc
import hashlib
import uuid as _uuid

import requests as _requests

from src.decoder import decode_bencode
from src.encoder import bencode_encode


@_dc.dataclass
class TrackingParams:
    info_hash: bytes
    peer_id: str
    left: int
    uploaded: int
    downloaded: int
    port: int = 6881
    compact: int = 1


@_dc.dataclass
class Peer:
    ip: str
    port: int


@_dc.dataclass
class TrackerResponse:
    peers: list[Peer]
    interval: int


def _parse_torrent_file(torrent_file: str) -> dict:
    """
    Parse a BitTorrent .torrent file and return its decoded contents.

    This function reads a .torrent file, decodes its bencoded content, and validates
    that it contains the required keys for a valid torrent file.

    Args:
        torrent_file (str): Path to the .torrent file to parse

    Returns:
        dict: The decoded torrent file contents as a dictionary

    Raises:
        ValueError: If the torrent file is invalid (not a dictionary, missing required keys)
        FileNotFoundError: If the torrent file doesn't exist
        IOError: If there are issues reading the file

    Example:
        >>> parsed = _parse_torrent_file("example.torrent")
        >>> print(parsed.keys())
        dict_keys(['announce', 'announce-list', 'comment', 'created by', 'creation date', 'info'])
    """
    with open(torrent_file, "rb") as f:
        bencoded_value = f.read()

    decoded_value = decode_bencode(bencoded_value)
    if not isinstance(decoded_value, dict):
        raise ValueError("Invalid torrent file: not a dictionary")

    if "info" not in decoded_value:
        raise ValueError("Invalid torrent file: missing 'info' key")

    if "announce" not in decoded_value:
        raise ValueError("Invalid torrent file: missing 'announce' key")

    return decoded_value


class TorrentFile:
    """
    A class to parse and access BitTorrent .torrent file information.

    This class provides a convenient interface to extract and work with the various
    components of a BitTorrent torrent file, including metadata, tracker information,
    and file details.

    For more information about the BitTorrent protocol and torrent file format,
    see: https://www.bittorrent.org/beps/bep_0003.html

    Attributes:
        torrent_file (str): The path to the original torrent file
        parsed (dict): The complete decoded torrent file contents
    """

    peer_id: str = _uuid.uuid4().hex[:20]

    def __init__(self, torrent_file: str):
        """
        Initialize a TorrentFile instance.

        Args:
            torrent_file (str): Path to the .torrent file to parse

        Raises:
            ValueError: If the torrent file is invalid
            FileNotFoundError: If the torrent file doesn't exist
        """
        self.torrent_file = torrent_file
        self.parsed = _parse_torrent_file(torrent_file)

    @property
    def info(self) -> dict:
        """
        Get the 'info' dictionary from the torrent file.

        The info dictionary contains metadata about the torrent, including:
        - piece length: size of each piece in bytes
        - pieces: concatenated SHA1 hashes of all pieces
        - name: suggested name for the download
        - files: list of files (for multi-file torrents)
        - length: total size in bytes (for single-file torrents)

        Returns:
            dict: The info dictionary containing torrent metadata

        Example:
            >>> torrent = TorrentFile("example.torrent")
            >>> info = torrent.info
            >>> print(f"Name: {info['name']}")
            >>> print(f"Piece length: {info['piece length']} bytes")
        """
        return self.parsed["info"]

    @property
    def announce(self) -> str:
        """
        Get the announce URL (tracker) from the torrent file.

        The announce URL is the primary tracker that coordinates peer discovery
        for this torrent. Clients use this URL to announce themselves and get
        a list of other peers.

        Returns:
            str: The announce URL for the torrent

        Example:
            >>> torrent = TorrentFile("example.torrent")
            >>> print(f"Tracker: {torrent.announce}")
            # Output: Tracker: https://tracker.example.com:1337/announce
        """
        return self.parsed["announce"]

    @property
    def info_hash_hex(self) -> str:
        """
        Calculate the SHA1 hash of the bencoded 'info' dictionary.

        The info hash is a unique identifier for the torrent and is used by
        trackers and peers to identify the specific torrent. It's calculated
        by SHA1-hashing the bencoded info dictionary.

        This hash is crucial for:
        - Torrent identification in the BitTorrent network
        - Tracker communication
        - Peer wire protocol handshakes

        Returns:
            str: The SHA1 hash of the info dictionary as a hexadecimal string

        Example:
            >>> torrent = TorrentFile("example.torrent")
            >>> print(f"Info hash: {torrent.info_hash}")
            # Output: Info hash: a1b2c3d4e5f6789012345678901234567890abcd
        """
        return hashlib.sha1(bencode_encode(self.info)).hexdigest()

    @property
    def info_hash_bytes(self) -> bytes:
        """
        Get the SHA1 hash of the bencoded 'info' dictionary as bytes.
        """
        return hashlib.sha1(bencode_encode(self.info)).digest()

    @property
    def piece_length(self) -> int:
        """
        Get the piece length (size of each piece) in bytes.

        Each torrent is divided into pieces of equal size (except possibly the last piece).
        A piece is usually 256 KB or 1 MB in size.

        This property returns the size of each piece in bytes.

        Returns:
            int: The size of each piece in bytes

        Example:
            >>> torrent = TorrentFile("example.torrent")
            >>> print(f"Piece length: {torrent.piece_length} bytes")
            # Output: Piece length: 262144 bytes (256 KB)
        """
        return self.info["piece length"]

    @property
    def pieces(self) -> list[str]:
        """
        Get the list of SHA1 hashes for all pieces in the torrent.

        The pieces property returns a list of hexadecimal SHA1 hashes, one for each
        piece in the torrent. Each piece hash is 40 characters long (20 bytes as hex).

        Each piece is assigned a SHA-1 hash value. On public networks, there may be malicious peers that send fake data.
        These hash values allow us to verify the integrity of each piece that we'll download.


        According to the BitTorrent specification:
        - pieces maps to a string whose length is a multiple of 20
        - It is subdivided into strings of length 20, each being the SHA1 hash of
          the piece at the corresponding index

        Reference: https://www.bittorrent.org/beps/bep_0003.html#info-dictionary

        Returns:
            list[str]: List of SHA1 hashes for each piece as hexadecimal strings

        Example:
            >>> torrent = TorrentFile("example.torrent")
            >>> pieces = torrent.pieces
            >>> print(f"Number of pieces: {len(pieces)}")
            >>> print(f"First piece hash: {pieces[0]}")
            # Output:
            # Number of pieces: 100
            # First piece hash: a1b2c3d4e5f6789012345678901234567890abcd
        """
        # TODO: Implement this
        return [
            self.info["pieces"][i : i + 20].hex()
            for i in range(0, len(self.info["pieces"]), 20)
        ]

    def _make_tracker_params(self) -> TrackingParams:
        """
        Make the tracker parameters.
        """
        return TrackingParams(
            info_hash=self.info_hash_bytes,
            peer_id=self.peer_id,
            port=6881,
            uploaded=0,
            downloaded=0,
            left=self.info["length"],
        )

    def _parse_peer(self, peer_bytes: bytes) -> Peer:
        """
        Parse a peer from a 6 bytes chunk.
        we can interpret a group of bytes as an integer by just putting them together left to right.

        Programming languages usually have library functions to convert byte arrays into integers,
        so you don't have to do this math yourself. You can use:

        hint:
            int.from_bytes(byte_array, byteorder="big", signed=False)
        """
        # TODO: Implement this
        ip_parts = [int.from_bytes(peer_bytes[i : i + 1], "big") for i in range(4)]
        ip = ".".join(str(part) for part in ip_parts)
        port = int.from_bytes(peer_bytes[4:6], "big")
        return Peer(ip, port)

    def _split_peers_bytes(self, peers_bytes: bytes) -> list[bytes]:
        """
        Split the peers bytes into 6 bytes chunks.
        """
        return [peers_bytes[i : i + 6] for i in range(0, len(peers_bytes), 6)]

    def get_tracker_response(self) -> TrackerResponse:
        """
        Get the list of peers from the torrent file.

        In each group, the first 4 bytes correspond to the IP address, where each byte represents a number in the IP address
        The last 2 bytes represent the port number, in big-endian order,
        meaning that we can interpret a group of bytes as an integer by just putting them together left to right.
        """
        params = self._make_tracker_params()
        response = _requests.get(self.announce, params=_dc.asdict(params))
        if response.status_code != 200:
            raise ValueError(f"Tracker returned status code {response.status_code}")

        resp = decode_bencode(response.content)

        peers_bytes = self._split_peers_bytes(resp["peers"])
        peers = [self._parse_peer(peer) for peer in peers_bytes]

        return TrackerResponse(
            peers=peers,
            interval=resp["interval"],
        )
