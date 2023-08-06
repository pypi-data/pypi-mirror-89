"""Implementation of the locate command."""

from mcipc.rcon.client import Client
from mcipc.rcon.je.errors import LocationNotFound
from mcipc.rcon.je.parsers.location import parse
from mcipc.rcon.je.types import Structure
from mcipc.rcon.response_types import Location


__all__ = ['locate']


def locate(client: Client, structure: Structure) -> Location:
    """Locates the respective structure."""

    response = client.run('locate', structure)

    try:
        return parse(response)
    except ValueError:
        raise LocationNotFound(structure) from None
