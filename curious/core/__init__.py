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
The core of Curious.

This package contains the bulk of the network interface with Discord, including parsing data that is incoming and 
delegating it to client code.

.. currentmodule:: curious.core

.. autosummary::
    :toctree: core
    
    client
    event
    gateway
    httpclient
    state
"""
import contextvars
import typing

if typing.TYPE_CHECKING:
    from curious.core.client import Client


_current_client = contextvars.ContextVar("current_client")

_current_shard = contextvars.ContextVar("current_shard")


def get_current_client() -> "Client":
    """
    Gets the currently running client. Mostly for internal usage.
    """

    return _current_client.get()
