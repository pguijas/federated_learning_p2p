#
# This file is part of the federated_learning_p2p (p2pfl) distribution (see https://github.com/pguijas/federated_learning_p2p).
# Copyright (c) 2022 Pedro Guijas Bravo.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""In-memory client."""

import random
import time
from typing import Dict, List, Optional, Union

from p2pfl.communication.client import Client
from p2pfl.communication.memory.memory_neighbors import InMemoryNeighbors
from p2pfl.communication.memory.server_singleton import ServerSingleton
from p2pfl.management.logger import logger
from p2pfl.settings import Settings


class NeighborNotConnectedError(Exception):
    """Neighbor not connected error."""

    pass


class InMemoryClient(Client):
    """Implementation of the client side of an in-memory communication protocol."""

    def __init__(self, self_addr: str, neighbors: InMemoryNeighbors) -> None:
        """Initialize the in-memory client."""
        self.__self_addr = self_addr
        self.__neighbors = neighbors

    def build_message(
        self, cmd: str, args: Optional[List[str]] = None, round: Optional[int] = None
    ) -> Dict[str, Union[str, int, List[str]]]:
        """Build a message."""
        if round is None:
            round = -1
        if args is None:
            args = []
        hs = hash(str(cmd) + str(args) + str(time.time()) + str(random.randint(0, 100000)))
        args = [str(a) for a in args]
        return {
            "source": self.__self_addr,
            "ttl": Settings.TTL,
            "hash": hs,
            "cmd": cmd,
            "args": args,
            "round": round,
        }

    def build_weights(
        self,
        cmd: str,
        round: int,
        serialized_model: bytes,
        contributors: Optional[List[str]] = None,
        weight: int = 1,
    ) -> Dict[str, Union[str, int, bytes, List[str]]]:
        """Build a weights message."""
        if contributors is None:
            contributors = []
        return {
            "source": self.__self_addr,
            "round": round,
            "weights": serialized_model,
            "contributors": contributors,
            "weight": weight,
            "cmd": cmd,
        }

    def send(
        self,
        nei: str,
        msg: Dict[str, Union[str, int, List[str], bytes]],
        create_connection: bool = False,
    ) -> None:
        """Send a message."""
        try:
            # Get neighbor
            try:
                node_server = self.__neighbors.get(nei)[1]
            except KeyError as e:
                raise NeighborNotConnectedError(f"Neighbor {nei} not found.") from e

            # Check if direct connection
            if node_server is None and create_connection:
                node_server = ServerSingleton()[nei]

            # Simulate sending a message by invoking the neighbor's receive function
            if node_server is not None:
                response = node_server.send_weights(msg) if "weight" in msg else node_server.send_message(msg)

            else:
                raise NeighborNotConnectedError(
                    "Neighbor not directly connected (Server not defined and create_connection is false)."
                )

            if "error" in response:
                logger.error(
                    self.__self_addr,
                    f"Error while sending a message: {msg['cmd']!r} {msg['args']!r}: {response['error']!r}",
                )
        except Exception as e:
            logger.info(
                self.__self_addr,
                f"Cannot send message {msg['cmd']!r} to {nei}. Error: {str(e)}",
            )
            print(msg)
            self.__neighbors.remove(nei)

    def broadcast(
        self,
        msg: Dict[str, Union[str, int, List[str], bytes]],
        node_list: Optional[List[str]] = None,
    ) -> None:
        """Broadcast a message."""
        # Node list
        nodes = node_list if node_list is not None else self.__neighbors.get_all(only_direct=True)

        # Send
        for n in nodes:
            self.send(n, msg)
