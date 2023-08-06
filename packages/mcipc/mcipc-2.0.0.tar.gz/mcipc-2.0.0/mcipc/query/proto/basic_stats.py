"""Basic statistics protocol."""

from __future__ import annotations
from typing import NamedTuple

from mcipc.query.proto.common import MAGIC
from mcipc.query.proto.common import decodeall
from mcipc.query.proto.common import ip_or_hostname
from mcipc.query.proto.common import random_session_id
from mcipc.query.proto.common import BigEndianSignedInt32
from mcipc.query.proto.common import IPAddressOrHostname
from mcipc.query.proto.common import Type


__all__ = ['Request', 'BasicStats', 'BasicStatsMixin']


class Request(NamedTuple):
    """Basic statistics request packet."""

    magic: bytes = MAGIC
    type: Type = Type.STAT
    session_id: BigEndianSignedInt32 = BigEndianSignedInt32()
    challenge_token: BigEndianSignedInt32 = BigEndianSignedInt32()

    def __bytes__(self):
        """Returns the packet as bytes."""
        payload = self.magic
        payload += bytes(self.type)
        payload += bytes(self.session_id)
        payload += bytes(self.challenge_token)
        return payload


class BasicStats(NamedTuple):
    """Basic statistics response packet."""

    type: Type
    session_id: BigEndianSignedInt32
    motd: str
    game_type: str
    map: str
    num_players: int
    max_players: int
    host_port: int
    host_ip: IPAddressOrHostname

    @classmethod
    def from_bytes(cls, bytes_: bytes) -> BasicStats:   # pylint: disable=R0914
        """Creates the packet from the respective bytes."""
        type_ = Type.from_bytes(bytes_[0:1])
        session_id = BigEndianSignedInt32.from_bytes(bytes_[1:5])
        *blocks, port_ip, _ = bytes_[5:].split(b'\0')
        motd, game_type, map_, num_players, max_players = decodeall(blocks)
        num_players = int(num_players)
        max_players = int(max_players)
        host_port = int.from_bytes(port_ip[0:2], 'little')
        host_ip = ip_or_hostname(port_ip[2:].decode())
        return cls(
            type_, session_id, motd, game_type, map_, num_players, max_players,
            host_port, host_ip)

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {
            'type': self.type.value,
            'session_id': self.session_id,
            'motd': self.motd,
            'game_type': self.game_type,
            'map': self.map,
            'num_players': self.num_players,
            'max_players': self.max_players,
            'host_port': self.host_port,
            'host_ip': str(self.host_ip)
        }


class BasicStatsMixin:  # pylint: disable=R0903
    """Query client mixin for basic stats."""

    @property
    def basic_stats(self) -> BasicStats:
        """Returns basic stats"""
        request = Request(
            session_id=random_session_id(),
            challenge_token=self.challenge_token)
        bytes_ = self.communicate(bytes(request))
        return BasicStats.from_bytes(bytes_)
