# Copyright (c) 2021 Johnathan P. Irvin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from typing import List

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect


class ConnectionManager:
    _connections: List[WebSocket] = []

    async def add_connection(self, connection: WebSocket) -> None:
        """
        Adds a connection to the list of connections.

        Args:
            connection (WebSocket): The connection to add.
        """
        await connection.accept()
        self._connections.append(connection)

    async def remove_connection(self, connection: WebSocket) -> None:
        """
        Removes a connection from the list of connections.

        Args:
            connection (WebSocket): The connection to remove.
        """
        try:
            await connection.close()
        except WebSocketDisconnect:
            pass

        self._connections.remove(connection)
    
    def get_connections(self: WebSocket) -> List[WebSocket]:
        """
        Returns the list of connections.

        Args:
            self (WebSocket): The connection manager.

        Returns:
            List[WebSocket]: The list of connections.
        """
        return self._connections

    async def broadcast(self, message: str) -> None:
        """
        Broadcasts a message to all connections.

        Args:
            message (str): The message to broadcast.
        """
        for connection in self._connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                self.remove_connection(connection)

