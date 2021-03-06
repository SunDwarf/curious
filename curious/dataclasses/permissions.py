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
Wrappers for Permission objects.

.. currentmodule:: curious.dataclasses.permissions
"""
from typing import Optional, Union

from curious.core import get_current_client
from curious.dataclasses import channel as dt_channel, member as dt_member, role as dt_role
from curious.exc import PermissionsError

target_thint = "Union[dt_member.Member, dt_role.Role]"


# RIP the generator.
class Permissions(object):
    """
    Represents the permissions a user can have.
    This type is automatically generated based upon a set of constant permission bits.

    Every permission is accessible via a property getter and setter. The raw permissions value is
    accessible via :attr:`.Permissions.bitfield`.
    """

    PERMISSION_MAPPING = {
        "create_instant_invite": 0,
        "kick_members": 1,
        "ban_members": 2,
        "administrator": 3,
        "manage_channels": 4,
        "manage_server": 5,
        "add_reactions": 6,
        "view_audit_log": 7,
        "read_messages": 10,
        "send_messages": 11,
        "send_tts_messages": 12,
        "manage_messages": 13,
        "embed_links": 14,
        "attach_files": 15,
        "read_message_history": 16,
        "mention_everyone": 17,
        "use_external_emojis": 18,
        "voice_connect": 20,
        "voice_speak": 21,
        "voice_mute_members": 22,
        "voice_deafen_members": 23,
        "voice_move_members": 24,
        "voice_use_voice_activation": 25,
        "change_nickname": 26,
        "manage_nicknames": 27,
        "manage_roles": 28,
        "manage_webhooks": 29,
        "manage_emojis": 30,
        # rest are unused
    }

    @staticmethod
    def __new__(cls, value: int = 0, **kwargs):
        if isinstance(value, cls):
            return value

        return super(Permissions, cls).__new__(cls)

    def __init__(self, value: int = 0, **kwargs):
        """
        Creates a new Permissions object.

        :param value: The bitfield value of the permissions object.
        """
        self.bitfield = value
        for perm, value in kwargs.items():
            if perm not in self.PERMISSION_MAPPING:
                raise ValueError("Unknown permission", perm)

            setattr(self, perm, value)

    def raise_for_permission(self, permission: str):
        """
        Raises an error if the specified permission is not set.
        """
        if not getattr(self, permission):
            raise PermissionsError(permission)

    def _get_bit(self, bit: int) -> bool:
        """
        Gets a bit from the internal bitfield of the permissions.
        """
        return bool((self.bitfield >> bit) & 1)

    def _set_bit(self, bit: int, value: bool):
        if value:
            self.bitfield |= 1 << bit
        else:
            self.bitfield &= ~(1 << bit)

    @classmethod
    def all(cls) -> "Permissions":
        """
        :return: A new Permissions object with all permissions.
        """
        return cls(9007199254740991)

    @classmethod
    def none(cls) -> "Permissions":
        """
        :return: A new permissions object with no permissions.
        """
        return cls(0)

    # Operator overloads.
    def __eq__(self, other) -> bool:
        if isinstance(other, int):
            return self.bitfield == other
        elif isinstance(self, Permissions):
            return self.bitfield == other.bitfield
        else:
            return NotImplemented

    def __repr__(self) -> str:
        # todo: make this better
        return "<Permissions value={}>".format(self.bitfield)

    def __str__(self):
        return self.__repr__()

    # Autogenerated

    @property
    def create_instant_invite(self) -> bool:
        """
        :return: If this member has the CREATE_INSTANT_INVITE permission (bit 0)
        """
        return self._get_bit(0)

    @create_instant_invite.setter
    def create_instant_invite(self, value: bool) -> None:
        self._set_bit(0, value)

    @property
    def kick_members(self) -> bool:
        """
        :return: If this member has the KICK_MEMBERS permission (bit 1)
        """
        return self._get_bit(1)

    @kick_members.setter
    def kick_members(self, value: bool) -> None:
        self._set_bit(1, value)

    @property
    def ban_members(self) -> bool:
        """
        :return: If this member has the BAN_MEMBERS permission (bit 2)
        """
        return self._get_bit(2)

    @ban_members.setter
    def ban_members(self, value: bool) -> None:
        self._set_bit(2, value)

    @property
    def administrator(self) -> bool:
        """
        :return: If this member has the ADMINISTRATOR permission (bit 3)
        """
        return self._get_bit(3)

    @administrator.setter
    def administrator(self, value: bool) -> None:
        self._set_bit(3, value)

    @property
    def manage_channels(self) -> bool:
        """
        :return: If this member has the MANAGE_CHANNELS permission (bit 4)
        """
        return self._get_bit(4)

    @manage_channels.setter
    def manage_channels(self, value: bool) -> None:
        self._set_bit(4, value)

    @property
    def manage_server(self) -> bool:
        """
        :return: If this member has the MANAGE_SERVER permission (bit 5)
        """
        return self._get_bit(5)

    @manage_server.setter
    def manage_server(self, value: bool) -> None:
        self._set_bit(5, value)

    @property
    def add_reactions(self) -> bool:
        """
        :return: If this member has the ADD_REACTIONS permission (bit 6)
        """
        return self._get_bit(6)

    @add_reactions.setter
    def add_reactions(self, value: bool) -> None:
        self._set_bit(6, value)

    @property
    def view_audit_log(self) -> bool:
        """
        :return: If this member has the VIEW_AUDIT_LOG permission (bit 7)
        """
        return self._get_bit(7)

    @view_audit_log.setter
    def view_audit_log(self, value: bool) -> None:
        self._set_bit(7, value)

    @property
    def read_messages(self) -> bool:
        """
        :return: If this member has the READ_MESSAGES permission (bit 10)
        """
        return self._get_bit(10)

    @read_messages.setter
    def read_messages(self, value: bool) -> None:
        self._set_bit(10, value)

    @property
    def send_messages(self) -> bool:
        """
        :return: If this member has the SEND_MESSAGES permission (bit 11)
        """
        return self._get_bit(11)

    @send_messages.setter
    def send_messages(self, value: bool) -> None:
        self._set_bit(11, value)

    @property
    def send_tts_messages(self) -> bool:
        """
        :return: If this member has the SEND_TTS_MESSAGES permission (bit 12)
        """
        return self._get_bit(12)

    @send_tts_messages.setter
    def send_tts_messages(self, value: bool) -> None:
        self._set_bit(12, value)

    @property
    def manage_messages(self) -> bool:
        """
        :return: If this member has the MANAGE_MESSAGES permission (bit 13)
        """
        return self._get_bit(13)

    @manage_messages.setter
    def manage_messages(self, value: bool) -> None:
        self._set_bit(13, value)

    @property
    def embed_links(self) -> bool:
        """
        :return: If this member has the EMBED_LINKS permission (bit 14)
        """
        return self._get_bit(14)

    @embed_links.setter
    def embed_links(self, value: bool) -> None:
        self._set_bit(14, value)

    @property
    def attach_files(self) -> bool:
        """
        :return: If this member has the ATTACH_FILES permission (bit 15)
        """
        return self._get_bit(15)

    @attach_files.setter
    def attach_files(self, value: bool) -> None:
        self._set_bit(15, value)

    @property
    def read_message_history(self) -> bool:
        """
        :return: If this member has the READ_MESSAGE_HISTORY permission (bit 16)
        """
        return self._get_bit(16)

    @read_message_history.setter
    def read_message_history(self, value: bool) -> None:
        self._set_bit(16, value)

    @property
    def mention_everyone(self) -> bool:
        """
        :return: If this member has the MENTION_EVERYONE permission (bit 17)
        """
        return self._get_bit(17)

    @mention_everyone.setter
    def mention_everyone(self, value: bool) -> None:
        self._set_bit(17, value)

    @property
    def use_external_emojis(self) -> bool:
        """
        :return: If this member has the USE_EXTERNAL_EMOJIS permission (bit 18)
        """
        return self._get_bit(18)

    @use_external_emojis.setter
    def use_external_emojis(self, value: bool) -> None:
        self._set_bit(18, value)

    @property
    def voice_connect(self) -> bool:
        """
        :return: If this member has the VOICE_CONNECT permission (bit 20)
        """
        return self._get_bit(20)

    @voice_connect.setter
    def voice_connect(self, value: bool) -> None:
        self._set_bit(20, value)

    @property
    def voice_speak(self) -> bool:
        """
        :return: If this member has the VOICE_SPEAK permission (bit 21)
        """
        return self._get_bit(21)

    @voice_speak.setter
    def voice_speak(self, value: bool) -> None:
        self._set_bit(21, value)

    @property
    def voice_mute_members(self) -> bool:
        """
        :return: If this member has the VOICE_MUTE_MEMBERS permission (bit 22)
        """
        return self._get_bit(22)

    @voice_mute_members.setter
    def voice_mute_members(self, value: bool) -> None:
        self._set_bit(22, value)

    @property
    def voice_deafen_members(self) -> bool:
        """
        :return: If this member has the VOICE_DEAFEN_MEMBERS permission (bit 23)
        """
        return self._get_bit(23)

    @voice_deafen_members.setter
    def voice_deafen_members(self, value: bool) -> None:
        self._set_bit(23, value)

    @property
    def voice_move_members(self) -> bool:
        """
        :return: If this member has the VOICE_MOVE_MEMBERS permission (bit 24)
        """
        return self._get_bit(24)

    @voice_move_members.setter
    def voice_move_members(self, value: bool) -> None:
        self._set_bit(24, value)

    @property
    def voice_use_voice_activation(self) -> bool:
        """
        :return: If this member has the VOICE_USE_VOICE_ACTIVATION permission (bit 25)
        """
        return self._get_bit(25)

    @voice_use_voice_activation.setter
    def voice_use_voice_activation(self, value: bool) -> None:
        self._set_bit(25, value)

    @property
    def change_nickname(self) -> bool:
        """
        :return: If this member has the CHANGE_NICKNAME permission (bit 26)
        """
        return self._get_bit(26)

    @change_nickname.setter
    def change_nickname(self, value: bool) -> None:
        self._set_bit(26, value)

    @property
    def manage_nicknames(self) -> bool:
        """
        :return: If this member has the MANAGE_NICKNAMES permission (bit 27)
        """
        return self._get_bit(27)

    @manage_nicknames.setter
    def manage_nicknames(self, value: bool) -> None:
        self._set_bit(27, value)

    @property
    def manage_roles(self) -> bool:
        """
        :return: If this member has the MANAGE_ROLES permission (bit 28)
        """
        return self._get_bit(28)

    @manage_roles.setter
    def manage_roles(self, value: bool) -> None:
        self._set_bit(28, value)

    @property
    def manage_webhooks(self) -> bool:
        """
        :return: If this member has the MANAGE_WEBHOOKS permission (bit 29)
        """
        return self._get_bit(29)

    @manage_webhooks.setter
    def manage_webhooks(self, value: bool) -> None:
        self._set_bit(29, value)

    @property
    def manage_emojis(self) -> bool:
        """
        :return: If this member has the MANAGE_EMOJIS permission (bit 30)
        """
        return self._get_bit(30)

    @manage_emojis.setter
    def manage_emojis(self, value: bool) -> None:
        self._set_bit(30, value)


perm_thint = Union[int, Permissions]


class Overwrite(object):
    """
    Represents a permission overwrite.

    This has all properties that the base Permissions object, but it takes into accounts the 
    overwrites for the channels. It is always recommended to use this over the server permissions, 
    as it will fall back to the default permissions for the role if it can't find specific 
    overwrites.

    The overwrite has a permission marked as ``True`` if the object has a) an overwrite on the 
    channel OR b) the object has that permission and no overwrite. The overwrite is marked as 
    ``False`` if the object has a) an overwrite on the channel OR b) the object does not have that 
    permission and no overwrite/a deny overwrite.

    You can set an attribute to None to clear the overwrite, True to set an allow overwrite, and 
    False to set a deny overwrite.

    .. warning::

        You probably don't want to create an instance of this class directly - instead, use
        :meth:`.Overwrite.overwrite_in(channel, target)`.

    """

    __slots__ = "target", "channel_id", "allow", "deny", "_immutable"

    @classmethod
    def overwrite_in(
        cls,
        channel: "dt_channel.Channel",
        target: target_thint,
        *,
        allow: perm_thint = None,
        deny: perm_thint,
    ) -> "Overwrite":
        """
        :param channel: The :class:`.Channel` to create this overwrite in.
        :param target: The :class:`.Member` or :class:`.Role` to create this overwrite for.
        :param allow: An optional set of allowed permissions.
        :param deny: An optional set of denied permissions.
        """
        allow = allow or 0
        deny = deny or 0
        return Overwrite(allow, deny, obb=target, channel_id=channel.id)

    def __init__(
        self,
        allow: Union[int, Permissions],
        deny: Union[int, Permissions],
        obb: "Union[dt_member.Member, dt_role.Role]",
        channel_id: int = None,
    ):
        """
        :param allow: A :class:`.Permissions` that this overwrite allows.
        :param deny: A :class:`.Permissions` that this overwrite denies.
        :param obb: Optional: The :class:`.Member` or :class:`.Role` that this overwrite is for.
        :param channel_id: Optional: The channel ID this overwrite is in.
        """
        self.target = obb
        self.channel_id = channel_id

        if isinstance(allow, Permissions):
            allow = allow.bitfield
        self.allow = Permissions(value=allow if allow is not None else 0)

        if isinstance(deny, Permissions):
            deny = deny.bitfield
        self.deny = Permissions(value=deny if deny is not None else 0)

        self._immutable = False

    @property
    def channel(self) -> "Optional[dt_channel.Channel]":
        """
        :return: The :class:`.Channel` this overwrite represents.
        """
        return get_current_client().state.find_channel(self.channel_id)

    def __repr__(self) -> str:
        return "<Overwrites for object={} channel={} allow={} deny={}>".format(
            self.target, self.channel, self.allow, self.deny
        )

    def __getattr__(self, item) -> bool:
        """
        Attribute getter helper.

        This will check allow first, the deny, then finally the role permissions.
        """
        if item == "_immutable":
            return super().__getattribute__("_immutable")

        if isinstance(self.target, dt_member.dt_user.User):  # lol
            permissions = Permissions(515136)
        elif isinstance(self.target, dt_member.Member):
            permissions = self.target.guild_permissions
        elif isinstance(self.target, dt_role.Role):
            permissions = self.target.permissions
        else:
            raise TypeError("Target must be a member or a role")

        if permissions.administrator:
            # short-circuit to always return True if they have administrator
            # this is because those overrides are useless
            # if the user wants to get the override, they can access `allow/deny` directly.
            return True

        if not hasattr(self.allow, item):
            raise AttributeError(item)

        if getattr(self.allow, item, None) is True:
            return True

        if getattr(self.deny, item, None) is True:
            # Return False because it's denied.
            return False

        return getattr(permissions, item, False)

    def __setattr__(self, key: str, value: object) -> object:
        """
        Attribute setter helper.
        """
        if key != "_immutable" and hasattr(self, "_immutable") and self._immutable:
            raise RuntimeError("This PermissionsOverwrite is immutable")

        if not hasattr(Permissions, key):
            super().__setattr__(key, value)
            return

        if value is False:
            setattr(self.deny, key, True)
        elif value is True:
            setattr(self.allow, key, True)
        elif value is None:
            setattr(self.allow, key, False)
            setattr(self.deny, key, False)
