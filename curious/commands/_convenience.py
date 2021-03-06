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
Convenience functions that are shortcuts for various context variable actions.
"""
import inspect
from os import PathLike
from typing import AsyncContextManager, Awaitable, Callable, IO, Union, List

from curious import Embed
from curious.commands.context import Context, current_command_context
from curious.dataclasses.message import Message

__all__ = [
    "send_message",
    "upload",
    "reply",
    "private_reply",
]

from curious.ext.paginator import ReactionsPaginator


async def send_message(content: str = None, **kwargs) -> Message:
    """
    Sends a message to the channel this command is running in.

    This passes arguments straight through to :meth:`.ChannelMessageWrapper.send`.

    :return: A :class:`.Message` that was sent to the channel.
    """
    ctx: Context = current_command_context.get()
    return await ctx.channel.messages.send(content=content, **kwargs)


async def reply(content: str = None, *, delimiter: str = ", ", **kwargs) -> Message:
    """
    Replies to the user that invoked the command.

    This passes arguments straight through to :meth:`.ChannelMessageWrapper.send`.

    :param delimiter: The delimiter to use between the mention and the content.
    :return: A :class:`.Message` that was sent to the channel.
    """
    ctx: Context = current_command_context.get()
    author = ctx.message.author.mention
    content = f"{author}{delimiter}{content}"
    return await ctx.channel.messages.send(content=content, **kwargs)


async def private_reply(content: str = None, **kwargs) -> Message:
    """
    Replies to the user that invoked the command in a private message.

    This passes arguments straight through to :meth:`.ChannelMessageWrapper.send`.

    :return: A :class:`.Message` tat was sent to the channel.
    """
    ctx: Context = current_command_context.get()
    author = ctx.message.author
    return await author.user.send(content=content, **kwargs)


async def upload(fp: "Union[bytes, str, PathLike, IO]", **kwargs) -> Message:
    """
    Uploads a message to the channel this command is running in.

    This passes arguments straight through to :meth:`.ChannelMessageWrapper.upload`.

    :return: A :class:`.Message` that was sent to the channel.
    """
    ctx: Context = current_command_context.get()
    return await ctx.channel.messages.upload(fp=fp, **kwargs)


async def wait_for_reply(
    predicate: Callable[[Message], Union[Awaitable[bool], bool]] = None,
) -> Message:
    """
    Waits for a reply from the author of this command.

    This will only accept replies from the original author in the original channel the command
    was ran in.

    :param predicate: An optional callable predicate.
    :return: The :class:`.Message` that was sent.
    """
    # this is called from at least 3 nested functions...
    # can only imagine the cellvar fuckery going on
    ctx: Context = current_command_context.get()

    async def _real_pred_pt2(message: Message):
        if message.author_id != ctx.message.author_id:
            return False

        if predicate:
            res = predicate(message)
            if inspect.isawaitable(res):
                res = await res

            return res

        return True

    return await ctx.channel.messages.wait_for_message(predicate=_real_pred_pt2)


async def paginate(content: Union[str, List[str], List[Embed]]):
    """
    Paginates some content.
    """
    ctx: Context = current_command_context.get()

    paginator = ReactionsPaginator(content=content, channel=ctx.channel, respond_to=ctx.author)
    return await paginator.paginate()


def typing() -> AsyncContextManager[None]:
    """
    An context manager that sends typing events whilst the block of code within runs.

    .. code-block:: python3

        async with typing():
            await some_long_operation()
    """
    ctx: Context = current_command_context.get()
    return ctx.channel.typing
