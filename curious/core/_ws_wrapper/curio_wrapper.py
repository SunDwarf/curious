# This file is part of curious.
#
# curious is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# curious is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with curious.  If not, see <http://www.gnu.org/licenses/>.

"""
A curio websocket wrapper.
"""
import curio
import threading
from curio.thread import AWAIT, async_thread
from functools import partial
from lomond import WebSocket
from lomond.events import Event, Poll
from lomond.persist import persist
from typing import AsyncIterator

from curious import USER_AGENT
from curious.core._ws_wrapper import BasicWebsocketWrapper


class CurioWebsocketWrapper(BasicWebsocketWrapper):
    """
    Wraps a lomond websocket in a thread.
    """

    def __init__(self, url: str) -> None:
        super().__init__(url)

        #: The gateway task running in an async thread.
        self._task = None  # type: curio.Task

        self._send_queue = curio.UniversalQueue()
        self._queue = curio.UniversalQueue()
        self._cancelled = threading.Event()
        self._ws = None  # type: WebSocket

    @async_thread
    def websocket_handler(self) -> None:
        """
        The actual websocket handler.

        This wraps the Lomond reconnecting websocket, putting data on the queue.
        """
        ws = WebSocket(self.url, agent=USER_AGENT)
        self._ws = ws
        # generate poll events every 0.5 seconds to see if we can cancel
        websocket = persist(ws, ping_rate=0, poll=0.5, exit_event=self._cancelled)
        for event in websocket:
            # on a poll event, consume from the queue and
            if isinstance(event, Poll):
                if not self._send_queue.empty():
                    next_send = self._send_queue.get()
                    next_send()
            else:
                self._queue.put(event)

        # signal the end of the queue
        self._queue.put(self._done)

    async def __aiter__(self) -> AsyncIterator[Event]:
        async for event in self._queue:
            if event is not self._done:
                yield event
            else:
                return

    async def send_text(self, message: str):
        """
        Sends text to the websocket.
        """
        p = partial(self._ws.send_text, message)
        await self._send_queue.put(p)

    async def close(self, code: int = 1000, reason: str = "Client disconnect",
                    reconnect: bool = False):
        """
        Cancels and closes this websocket.
        """
        def _close():
            # if reconnecting, don't close this as this will kill the websocket prematurely
            if not reconnect:
                self._cancelled.set()
                AWAIT(self._task.cancel(blocking=False))  # don't block because it closes by itself

            self._ws.close(code=code, reason=reason)

        await self._send_queue.put(_close)

    @classmethod
    async def open(cls, url: str) -> 'BasicWebsocketWrapper':
        """
        Opens a websocket to the specified URL.
        """
        obb = cls(url)
        task = await curio.spawn(obb.websocket_handler())
        obb._task = task
        return obb
